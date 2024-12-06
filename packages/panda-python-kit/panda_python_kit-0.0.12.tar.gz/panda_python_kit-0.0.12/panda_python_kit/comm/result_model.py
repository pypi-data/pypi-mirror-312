
class ResultModel:
    def __init__(self,success=True,data=None,message=""):
        self.success = success
        self.data = data
        self.message = message

    def __str__(self):
        return "success:%s,data:%s,message:%s" % (self.success,self.data,self.message)