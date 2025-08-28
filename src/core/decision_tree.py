class DecisionNode:
    def __init__(self, attr=None, value=None, filhos=None, action=None):
        self.attr = attr
        self.value = value
        self.filhos = filhos or []
        self.action = action
        
    def eh_folha(self):
        return self.action is not None
    
    def classificar(self, attr):
        if self.eh_folha():
            self.action(attr)
            return
        
        value = attr.get(self.attr)
        for filho in self.filhos:
            if filho.value == value:
                return filho.classificar(attr)
        print("Regra não encontrada.")