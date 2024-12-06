from typing import Any, Dict, List

import numpy as np
import pandas as pd

from assonant.data_classes.enums import ExperimentStage

from ..enums import AcquisitionType, CSVColumn, ValuePlaceholders
from ..exceptions import AssonantDataParserError
from ._assonant_data_parser_interface import IAssonantDataParser


class CSVDataParser(IAssonantDataParser):

    def __init__(self, config_file_path: str):

        self.df = pd.read_csv(config_file_path, sep=",", header=1)

        self._clean_data()

        self._pre_process()

    def _clean_data(self):
        """Apply data cleaning steps over dataframe. This methods should focus on steps which will make some
        kind of row/column removal/drop for some reason (e.g: Rows with not accept values).

        Raises:
            AssonantDataParserError: Raised when a problem occurs in any of the data cleaning steps
        """
        try:
            # Remove all rows related to Experiment. Temporary limitation for tests!
            self.df = self.df[self.df[CSVColumn.CLASS.value] != "Experiment"]
        except Exception as e:
            raise AssonantDataParserError("[CLEAN-DATA] CSV data parser failed while filtering columns!") from e
        # pass # No data cleaning currently needed

    def _pre_process(self):
        """Apply pre-processing steps over dataframe. This methods should focus on steps which will make some kind
        of transformation over data from the Dataframe (e.g: Transform field values into str type).

        Raises:
            AssonantDataParserError: Raised when a problem occurs in any of the pre-processing steps
        """
        # Transform Name and Class column on lower case
        try:
            # Transform all 'Name' strings into lowercase to avoid type error from users
            self.df[CSVColumn.NAME.value] = self.df[CSVColumn.NAME.value].apply(lambda x: x.lower())
        except Exception as e:
            raise AssonantDataParserError(
                f"[PRE-PROCESS] CSV data parser failed while lowering {CSVColumn.NAME.value} column strings! The cause may be a row with a missing value!"
            ) from e
        try:
            # Transform all 'Subcomponent of' strings into lowercase to correctly match 'Name' that
            # has just been lowercased
            self.df[CSVColumn.SUBCOMPONENT_OF.value] = self.df[CSVColumn.SUBCOMPONENT_OF.value].apply(
                lambda x: x.lower() if isinstance(type(x), str) else x
            )
        except Exception as e:
            raise AssonantDataParserError(
                f"[PRE-PROCESS] CSV data parser failed while lowering {CSVColumn.SUBCOMPONENT_OF.value} column strings!"
            ) from e
        try:
            # Remove empty space between names to match AssonantDataClass names
            self.df[CSVColumn.CLASS.value] = self.df[CSVColumn.CLASS.value].apply(lambda x: x.replace(" ", ""))
        except Exception as e:
            raise AssonantDataParserError(
                f"[PRE-PROCESS] CSV data parser failed while concatenating {CSVColumn.CLASS.value} column strings! The cause may be a row with a missing value!"
            ) from e
        try:
            # Replace np.nan value to None
            self.df = self.df.replace(np.nan, None)
        except Exception as e:
            raise AssonantDataParserError(
                "[PRE-PROCESS] CSV data parser failed while converting np.nan values to None!"
            ) from e
        # try:
        #    # Convert Experiment class to Entry class
        #    self.df[CSVColumn.CLASS.value] = self.df[CSVColumn.CLASS.value].replace('Experiment', 'Entry')
        # except Exception as e:
        #    raise AssonantDataParserError(
        #        "[PRE-PROCESS] CSV data parser failed while converting np.nan values to None!"
        #    ) from e

    def _get_row_by_pv_name(self, pv_name: str) -> pd.DataFrame:
        """Return DataFrame row that matches the passed PV name.

        Args:
            pv_name (str): PV name that identified the target row.

        Returns:
            pd.DataFrame: DataFrame row that matches the passed pv_name.
        """
        # Find row that matches the PV name and return a copy of it
        return self.df[self.df[CSVColumn.PV_NAME.value] == pv_name].copy(deep=True)

    def _convert_experiment_stage_into_acquisition_type(self, experiment_stage: ExperimentStage) -> AcquisitionType:

        mapping = {
            ExperimentStage.START.value: AcquisitionType.SNAPSHOT,
            ExperimentStage.END.value: AcquisitionType.SNAPSHOT,
            ExperimentStage.DURING.value: AcquisitionType.SCAN
        }
        try:
            converted_value = mapping[experiment_stage.value]
        except Exception as e:
            raise AssonantDataParserError(
                f"There currently no valid AcquisitionType convertion value for '{experiment_stage.value}' ExperimentStage"
            ) from e
        return converted_value

    def get_pv_names_by_experiment_stage(self, experiment_stage: ExperimentStage) -> List[str]:
        """Return a List with all PV names related to the passed ExperimentStage.

        PS: Check IAssonantDataParser Interface for the return structure definition!

        Args:
            acquisition_type (ExperimentStage): Target experiment stage used for selecting which
            PV names will be returned.

        Returns:
            List[str]: List containing all PV names related to passed ExperimentStage.
        """
        acquisition_type = self._convert_experiment_stage_into_acquisition_type(experiment_stage)
        filtered_df = self.df[self.df[CSVColumn.ACQUISITION_TYPE.value] == acquisition_type.value]
        filtered_df = filtered_df[
            ~filtered_df[CSVColumn.PV_NAME.value].isin([""]) & filtered_df[CSVColumn.PV_NAME.value].notna()
        ]

        # Iterate over rows and append the PV name to the result List
        result = [row[CSVColumn.PV_NAME.value] for _, row in filtered_df.iterrows()]
        return result

    def get_pvs_info(self, pv_names: List[str]) -> Dict[str, Dict[str, Any]]:
        """Return all information about the PV paired by the its name.

        PS: Check IAssonantDataParser Interface for the return structure definition!

        Args:
            pv_names (List[str]): List with PV names which data field info will be fetched.

        Returns:
            Dict[str, Dict[str, Any]]: Dictionary containing all PV data paired by the PV name.
        """
        invalid_values = [None, np.nan, ""]
        filtered_df = self.df[self.df[CSVColumn.PV_NAME.value].isin(pv_names)]

        result = {
            row[CSVColumn.PV_NAME.value]: {
                "component_info": {
                    "name": row[CSVColumn.NAME.value],
                    "class": row[CSVColumn.CLASS.value],
                    **(
                        {"subcomponent_of": row[CSVColumn.SUBCOMPONENT_OF.value]}
                        if row[CSVColumn.SUBCOMPONENT_OF.value] not in invalid_values
                        else {}
                    ),
                },
                "data_handler_info": {
                    "name": row[CSVColumn.NEXUS_FIELD_NAME.value],
                    "value": ValuePlaceholders.VALUE_NOT_SET.value,
                    **(
                        {"unit": row[CSVColumn.UNIT_OF_MEASUREMENT.value]}
                        if row[CSVColumn.UNIT_OF_MEASUREMENT.value] not in invalid_values
                        else {}
                    ),
                    **(
                        {"transformation_type": row[CSVColumn.TRANSFORMATION_TYPE.value]}
                        if row[CSVColumn.TRANSFORMATION_TYPE.value] not in invalid_values
                        else {}
                    ),
                    "pv_name": row[CSVColumn.PV_NAME.value],
                },
            }
            for _, row in filtered_df.iterrows()
        }

        return result
