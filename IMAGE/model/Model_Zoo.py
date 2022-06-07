from torchvision.models import wide_resnet50_2, resnet18


class Pretrain_model:
    def __init__(self, method = "resnet18"):
        self.method = method
        self.t_d,self.d, self.model = 0,0,0

    def call(self):
        if(self.method == 'resnet18'):
            print("resnet18 모델을 로드했습니다.")
            self.model = resnet18(pretrained=True, progress=True)
            self.t_d = 448
            self.d = 100
        elif(self.method == 'wide_resnet50_2'):
            print("wide_resnet50_2 모델을 로드했습니다.")
            self.model = wide_resnet50_2(pretrained=True, progress=True)
            self.t_d = 1792
            self.d = 550
        else:
            print("존재하지 않는 모델을 입력했습니다.")

        return self.model, self.t_d, self.d
# A = Pretrain_model(method="wide_resnet50_2")
# print(A.call())
