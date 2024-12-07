from ...metric_results.data_quality import NumericalColumnDataInfoResult
from ...metric_results.data_quality import get_info_numerical_column
from ...metric_results.data_quality import CategoricalColumnDataInfoResult
from ...metric_results.data_quality import CorrelationInfoResults
from ...metric_results.data_quality import calculate_correlation_pipeline
from ...metric_results.data_quality import get_info_categorical_column


from typing import Dict, Union, Optional
from evidently import ColumnMapping
from evidently.base_metric import MetricResult
from evidently.base_metric import Metric, InputData
from evidently.renderers.base_renderer import MetricRenderer, default_renderer

class DataQualityResults(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:DataQualityResults"
    current_data_quality: Dict[str, Union[NumericalColumnDataInfoResult, CategoricalColumnDataInfoResult]]
    reference_data_quality: Optional[Dict[str, Union[NumericalColumnDataInfoResult, CategoricalColumnDataInfoResult]]]
    correlation: Dict[str, CorrelationInfoResults]

class DataQualityMetric(Metric[DataQualityResults]):
    class Config:
        type_alias = "evidently:metric:DataQualityMetric"

    def __init__(self):
        super().__init__()

    def calculate(self, data: InputData) -> DataQualityResults:
        if data.current_data is None:
            raise ValueError("Current dataset should be present")

        current_data_quality = {}
        reference_data_quality = {}
        correlation = {}
        column_mapping = data.column_mapping

        # Process categorical features
        for column in column_mapping.categorical_features:
            if data.reference_data is not None:
                reference_data_quality[column] = get_info_categorical_column(data.reference_data[column])
            current_data_quality[column] = get_info_categorical_column(data.current_data[column])

        # Process numerical features
        for column in column_mapping.numerical_features:
            if data.reference_data is not None:
                reference_data_quality[column] = get_info_numerical_column(data.reference_data[column])
            current_data_quality[column] = get_info_numerical_column(data.current_data[column])

        # Correlation
        if data.reference_data is not None:
            correlation['reference'] = calculate_correlation_pipeline(
                data=data.reference_data, 
                categorical_features=column_mapping.categorical_features, 
                numerical_features= column_mapping.numerical_features)
            correlation['current'] =  calculate_correlation_pipeline(
                data=data.current_data, 
                categorical_features=column_mapping.categorical_features, 
                numerical_features= column_mapping.numerical_features)
    
        return DataQualityResults(
            current_data_quality=current_data_quality,
            reference_data_quality=reference_data_quality if data.reference_data is not None else None,
            correlation=correlation
        )


@default_renderer(wrap_type=DataQualityMetric)
class DataQualityRender(MetricRenderer):
    def render_json(self, obj: DataQualityMetric, include_render: bool = False,
        include: "IncludeOptions" = None, exclude: "IncludeOptions" = None,) -> dict:
        result = obj.get_result().get_dict(include_render, include, exclude)
        return result
