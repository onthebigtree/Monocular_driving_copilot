
from test_simple import predict_depth

def run_depth_prediction(image_path = "../system_db/id_1/1_disp.jpeg", model_name = "mono+stereo_640x192", pred_metric_depth =True):
    return predict_depth(image_path)


result = run_depth_prediction()
print(result)
