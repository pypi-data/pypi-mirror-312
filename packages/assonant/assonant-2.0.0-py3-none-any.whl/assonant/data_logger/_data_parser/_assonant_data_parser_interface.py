from abc import ABC, abstractmethod
from typing import Any, Dict, List

from assonant.data_classes.enums import ExperimentStage


class IAssonantDataParser(ABC):
    """Assonant Data Parser Interface.

    This interface defines what must be implemented by a class to be a Data Parser
    in Assonant environment.
    """

    @abstractmethod
    def get_pv_names_by_experiment_stage(self, experiment_stage: ExperimentStage) -> List[str]:
        """Return a List with all PV names related to the passed ExperimentStage.

        Returned Structure Definition:
        [
            PV_1_NAME,
            PV_2_NAME,
            PV_3_NAME,
            ...
            PV_N_NAME
        ]

        Args:
            experiment_stage (ExperimentStage): Target experiment stage used for selecting which
            PV names will be returned.

        Raises:
            AssonantDataParserError: Failure to retrieve requested data.

        Returns:
            List[str]: List containing all PV names related to passed ExperimentStage.
        """

    @abstractmethod
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
