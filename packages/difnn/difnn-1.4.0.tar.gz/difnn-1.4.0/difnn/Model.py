import pandas as pd

from difnn.forecast_utility import DIFNN, ExogClassificationStrategy, ExogRegressionStrategy

def fit_and_predict(time_series: pd.DataFrame,
                    exog_classification: list[pd.DataFrame],
                    exog_regression: list[pd.DataFrame],
                    horizon: int,
                    show_graph: bool = False):
    model = DIFNN()
    forecast_df, exog_effects = model.fit_and_predict(dataframe=time_series,
                                                      with_optimization=False,
                                                      horizon=horizon,
                                                      exog_classification={
                                                        'strategy': ExogClassificationStrategy.Mode9,
                                                        'data': exog_classification
                                                      } if exog_classification is not None else None,
                                                      exog_regression={
                                                        'strategy': ExogRegressionStrategy.Mode3,
                                                        'data': exog_regression
                                                      } if exog_regression is not None else None,
                                                      show_graph=show_graph)
    
    #model = DIFNN()
    #forecast_df, exog_effects = model.fit_and_predict(time_series=time_series,
    #                                                  with_optimization=True,
    #                                                  horizon=horizon,
    #                                                  exog_classification={
    #                                                    'strategy': ExogClassificationStrategy.Mode7,
    #                                                    'data': exog_classification
    #                                                  } if exog_classification is not None else None,
    #                                                  exog_regression={
    #                                                    'strategy': ExogRegressionStrategy.Mode3,
    #                                                    'data': exog_regression
    #                                                  } if exog_regression is not None else None,
    #                                                  show_graph=show_graph)
    
    return forecast_df, exog_effects