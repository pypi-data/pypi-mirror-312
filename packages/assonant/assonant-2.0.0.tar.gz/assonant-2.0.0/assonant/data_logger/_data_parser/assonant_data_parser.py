from typing import Any, Dict, List

from assonant.data_classes.enums import ExperimentStage

from ..exceptions.data_parsers_exceptions import AssonantDataParserError
from ._assonant_data_parser_interface import IAssonantDataParser
from ._data_parser_factory import DataParserFactory


class AssonantDataParser(IAssonantDataParser):
    """Assonant Data Parser. Wrapper class to deal with parsing config files and instatiating components and fields.

    Wrapper class that abstracts all process related to creating specific data parsers, parsing config files of
    specific formats and instatiating components and fields given parsed config file.
    """

    _factory = DataParserFactory()

    def __init__(self, config_file_path: str):

        # Persist passed config_file_path
        self.config_file_path = config_file_path

        self.data_parser = self._factory.create_data_parser(config_file_path)

    def get_pv_names_by_experiment_stage(self, experiment_stage: ExperimentStage) -> List[str]:
        """Return a List with all PV names related to the passed ExperimentStage.

        Example of returned structure: [PV1_NAME, PV2_NAME, ...]

        Args:
            experiment_stage (ExperimentStage): Target experiment stage used for selecting which
            PV names will be returned.

        Raises:
            AssonantDataParserError: Failure to retrieve requested data.

        Returns:
            List[str]: List containing all PV names related to passed ExperimentStage.
        """
        try:
            return self.data_parser.get_pv_names_by_experiment_stage(experiment_stage)
        except Exception as e:
            raise AssonantDataParserError(
                f"Failed to retrieve PV names from {self.config_file_path} for '{experiment_stage}' experiment stage"
            ) from e

    def get_pvs_info(self, pv_names: List[str]) -> Dict[str, Dict[str, Any]]:
        """Return all information about the PV paired by the its name.

        Example of return structure.:
        {
            PV_1_NAME_: {
                component_info:
                {
                    name: COMPONENT_NAME,
                    class: COMPONENT_CLASS
                    subcomponent_of: ASCENDANT_COMPONENT_NAME (if exists)
                },
                data_handler_info:
                {
                    name: FIELD_NAME,
                    value: PLACEHOLDER_VALUE
                    unit: FIELD_UNIT (if exists),
                    transformation_type: FIELD_TRANSFORMATION_TYPE (if exists),
                    PV_1_EXTRA_METADATA_1_NAME: PV_1_EXTRA_METADATA_1_VALUE (if exists),
                    PV_1_EXTRA_METADATA_2_NAME: PV_1_EXTRA_METADATA_2_VALUE (if exists),
                    ...
                }
            },
            PV_2_NAME_: {
                component_info:
                {
                    name: COMPONENT_NAME,
                    class: COMPONENT_CLASS
                    subcomponent_of: ASCENDANT_COMPONENT_NAME (if exists)
                },
                data_handler_info:
                {
                    name: FIELD_NAME,
                    value: PLACEHOLDER_VALUE
                    unit: FIELD_UNIT (if exists),
                    transformation_type: FIELD_TRANSFORMATION_TYPE (if exists),
                    PV_2_EXTRA_METADATA_1_NAME: PV_2_EXTRA_METADATA_1_VALUE (if exists),
                    PV_2_EXTRA_METADATA_2_NAME: PV_2_EXTRA_METADATA_2_VALUE (if exists),
                    ...
                }
            },
        }

        Args:
            pv_names (List[str]): List with PV names which data field info will be fetched.

        Returns:
            Dict[str, Dict[str, Any]]: Dictionary containing all PV info paired by the PV name.
        """
        try:
            return self.data_parser.get_pvs_info(pv_names)
        except Exception as e:
            raise AssonantDataParserError(f"Failed to retrieve pvs info from {self.config_file_path}") from e
