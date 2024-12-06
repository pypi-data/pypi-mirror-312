import os.path
from typing import Any, Dict, List, Type, Union

import numpy as np

from assonant.data_classes import (
    AssonantComponentFactory,
    AssonantDataHandlerFactory,
    Entry,
)
from assonant.data_classes.components import Beamline, Component
from assonant.data_classes.data_handlers import Axis, DataField, DataHandler
from assonant.data_classes.enums import BeamlineName, ExperimentStage
from assonant.data_classes.exceptions import AxisInsertionError, FieldInsertionError
from assonant.file_writer import AssonantFileWriter

from ._data_parser import AssonantDataParser
from ._pv_collector import PVCollector
from .exceptions import AssonantDataLoggerError


class AssonantDataLogger:
    """Assonant Data Logger.

    Object responsible to automatize data collection, standardization and logging based on
    pré-defined configurations.
    """

    _supported_experiment_stages_for_auto_collection = [ExperimentStage.START, ExperimentStage.END]

    def __init__(
        self,
        beamline_name: BeamlineName,
        config_file_path: str,
        config_file_name: str,
        log_file_path: str,
        log_file_name: str,
        pre_init_auto_collector_pv_connections: bool = False
    ):
        """AssonantDataLogger Constructor.

        Args:
            beamline_name (BeamlineName): Beamline name where the experiment is being executed.
            config_file_path (str): Path to configuration file.
            config_file_name (str): Name of the configuration file.
            log_file_path (str): Path where log file will be sastved.
            log_file_name (str): Name that will be given to log file.
            pre_init_auto_collector_pv_connections (bool): Flag to control if connections to auto collectable PVs should
            be pre-initiallized during AssonantDataLogger instantiation or not. Defaults to False. 
        """

        self.beamline_name = beamline_name.value
        self.log_file_path = log_file_path
        self.log_file_name = log_file_name
        self.data_parser = AssonantDataParser(os.path.join(config_file_path, config_file_name))
        self.pv_names = {}
        self.pv_collectors = {}
        self.file_writer = AssonantFileWriter("nexus")
        self.pv_collectors_innitialized = False
        
        if pre_init_auto_collector_pv_connections is True:
            self.init_auto_collector()

    def _create_data_handler_from_pv_info(self, pv_info: Dict[str, Dict[str, Any]]) -> DataHandler:
        """Create data handler based on passed pv_info Dict.

        Args:
            pv_info (Dict[str, Dict[str, Any]]): Dict containing acquired PV info. The Dict follows must follow
            the structure proposed for the get_pvs_info() call from the IAssonantDataParser Interface.

        Returns:
            DataHandler: Specific DataHandler related to the passed info.
        """
        param_names = ["value", "unit", "transformation_type", "timestamps", "timestamps_unit"]
        ignored = ["name"]
        extra_metadata = {}
        params = {}

        # Search into dict which names are parameters for the create method from factory, the rest
        # is considered as extra_metadata
        data_handler_info = pv_info["data_handler_info"]
        for info_name in data_handler_info:
            if info_name not in ignored:
                if info_name not in param_names:
                    extra_metadata[info_name] = data_handler_info[info_name]
                else:
                    params[info_name] = data_handler_info[info_name]

        params["extra_metadata"] = extra_metadata

        return AssonantDataHandlerFactory.create_data_handler(**params)

    def _set_data_handler_value(
        self, data_handler: DataHandler, value: Union[int, float, str, List, Type[np.ndarray], None]
    ) -> DataHandler:
        """Set value to DataHandler based on which type of DataHandler it is.

        Args:
            data_handler (DataHandler): DataHandler objct which value will be set.
            value (Union[int, float, str, List, Type[np.ndarray], None]): Value to be set to the value field
            of passed DataHandler

        Returns:
            DataHandler: DataHandler with new value set to its value field.
        """
        if isinstance(data_handler.value, DataField):
            data_handler.value.value = value
        else:
            data_handler.value = value

        return data_handler

    def _add_fields_to_component(self, component: Component, fields: dict[str, DataHandler]):
        """Add fields from dict to passed Component.

        Args:
            component (Component): Component which fields will be inserted to.
            fields (dict[str, DataHandler]): Dict of fields that will be inserted on component.
        """

        for field_name in fields:
            try:
                component.add_field(name=field_name, new_field=fields[field_name])
            except FieldInsertionError:
                # To avoid breaking and not logging other data, errors in insertion are ignored and logged
                # TODO: Put this into a log file instead of printing it
                print(
                    f"{field_name} field was not add to {component.name} due to an Error during its insertion on fields dict"
                )

    def _add_positions_to_component(self, component: Component, positions: dict[str, Axis]):
        """Add axis from dict to passed Component.

        Args:
            component (Component): Component which axis will be inserted to.
            positions (dict[str, Axis]): Dict of axis that will be inserted on component.
        """

        for axis_name in positions:
            try:
                component.add_position(name=axis_name, new_axis=positions[axis_name])
            except AxisInsertionError:
                # To avoid breaking and not logging other data, errors in insertion are ignored and logged
                # TODO: Put this into a log file instead of printing it
                print(
                    f"{axis_name} Axis was not add to {component.name} due to an Error during its insertion on positions dict"
                )

    def _create_component_from_pv_info(self, pv_info: Dict[str, Dict[str, Any]]) -> Component:

        component_info = pv_info["component_info"]
        return AssonantComponentFactory.create_component_by_class_name(
            class_name=component_info["class"], component_name=component_info["name"]
        )

    def _wrap_components_into_entry(self, components: List[Component], experiment_stage: ExperimentStage) -> Entry:
        """Wrap components into a Entry object based on the ExperimentStage.

        Args:
            components (List[Component]): List of Components to wrap into the Entry object.
            experiment_stage (ExperimentStage): The experiment stage which components data were collected.

        Returns:
            Entry: Entry containing all passed components within a Beamline object.
        """
        beamline = Beamline(name=self.beamline_name)
        beamline.create_and_add_field(
            name="name", value=self.beamline_name
        )  # Force name field based on DataLogger config
        entry = Entry(experiment_stage=experiment_stage, beamline=beamline)

        for component in components:

            if isinstance(component, Entry):
                # Special case: Metadata related to Entry must be added to pre-created instance
                entry.take_data_handlers_from(entry=entry)
            elif isinstance(component, Beamline):
                # Special case: Metadata related to beamline must be added to pre-created instance
                beamline.take_data_handlers_from(component=component)
            else:
                beamline.add_subcomponent(component)

        return entry
    
    def init_auto_collector(self):
        """Initialized PV collectors for auto collection functionality."""
        
        experiment_stages = [ExperimentStage.START, ExperimentStage.END]

        for experiment_stage in experiment_stages:
            
            # Try to retrieve PV names that will be collect on experiment stage
            try: 
                self.pv_names[experiment_stage.value] = self.data_parser.get_pv_names_by_experiment_stage(
                    experiment_stage
                )
            except Exception as e:
                raise AssonantDataLoggerError(
                    f"Failed to retrieve PV names for '{experiment_stage.value}' experiment stage!"
                ) from e

            # Try to initialize connection retrieve PVs
            try:
                self.pv_collectors[experiment_stage.value] = PVCollector(self.pv_names[experiment_stage.value])
            except Exception as e:
                raise AssonantDataLoggerError(
                    f"Faield to initialize PVCollector for PVs from '{experiment_stage.value}' experiment stage!"
                ) from e

        # Update PV collector status flag
        self.pv_collectors_innitialized = True

    def collect_and_log_pv_data(self, experiment_stage: ExperimentStage):
        """Trigger data logger to collect PV data based on ExperimentStage, standardize it and log it.

        Args:
            experiment_stage (ExperimentStage): ExperimentStage which PV data will be collected and logged.

        """
        if experiment_stage in self._supported_experiment_stages_for_auto_collection:
            if self.pv_collectors_innitialized is False:
                self.init_auto_collector()
            acquired_pv_data = self.pv_collectors[experiment_stage.value].acquire_data()
            self.log_collected_pv_data(experiment_stage=experiment_stage, pv_data=acquired_pv_data)
        else:
            raise AssonantDataLoggerError(
                f"Experimental stage '{experiment_stage.value}' is not supported yet for auto collection! Use the log_collected_data method instead!"
            )

    def log_collected_pv_data(self, experiment_stage: ExperimentStage, pv_data: Dict[str, Any]):
        """Standardize and log collected PV data represented as {PV_NAME: COLLECTED_VALUE} Dict.

        Args:
            experiment_stage (ExperimentStage): Current ExperimentStage which data was collected.
            pv_data (Dict[str, Any]): Collected PV data. The Dict structure must follow the same data structure
            and representation as the PVCollector acquire_data() method.
        """
        pv_names = [pv_name for pv_name in pv_data.keys()]
        pv_name_and_info_mapping = self.data_parser.get_pvs_info(pv_names=pv_names)
        components = {}

        # Create DataHandlers for each acquired PV
        for pv_name, pv_info in pv_name_and_info_mapping.items():

            # Create DataHandler for PV field
            data_handler = self._create_data_handler_from_pv_info(pv_info)
            self._set_data_handler_value(data_handler, pv_data[pv_name])
            data_handler_name = pv_info["data_handler_info"]["name"]

            component_name = pv_info["component_info"]["name"]

            # Create Component if doesn't already exist
            if component_name not in components.keys():
                components[component_name] = self._create_component_from_pv_info(pv_info)

            components[component_name].add_data_handler(name=data_handler_name, new_data_handler=data_handler)

        entry = self._wrap_components_into_entry(list(components.values()), experiment_stage)

        self.file_writer.write_data(self.log_file_path, self.log_file_name, entry)

    def log_collected_component_data(
        self, experiment_stage: ExperimentStage, components: Union[Component, List[Component]]
    ):
        """Standardize and log collected PV data already wrapped as Assonant Components.

        Args:
            experiment_stage (ExperimentStage):  Current ExperimentStage which data was collected.
            components (Union[Component, List[Component]]): _description_
        """
        if isinstance(components, Component):
            components = [components]

        entry = self._wrap_components_into_entry(components, experiment_stage)
        self.file_writer.write_data(self.log_file_path, self.log_file_name, entry)
