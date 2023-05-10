import net
import torch

from config import PATH_MODEL_IR50, PATH_MODEL_IR101


class Model:
    def __init__(self):
        self.adaface_models = {
            'ir_50': "Model/adaface_ir50_webface4m.ckpt",
            'ir_101': "Model/finetune_ir101_webface4m.ckpt"
        }

    def load_pretrained_model(self, architecture='ir_50'):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # load model and pretrained statedict
        assert architecture in self.adaface_models.keys()
        # build model
        model = net.build_model(architecture)
        # load statedict
        statedict = torch.load(self.adaface_models[architecture], map_location=device)['state_dict']
        model_statedict = {key[6:]: val for key, val in statedict.items() if key.startswith('model.')}
        model.load_state_dict(model_statedict)
        model.eval()
        return model
