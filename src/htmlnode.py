class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is not None and self.props != {}:
            attribs = ""
            for k,v in self.props.items():
                attribs = attribs+f' {k}="{v}"'
            return attribs
        else:
            return ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf has no 'Value'")
        if self.tag == None:
            return self.value
        else:
            return "<" + self.tag + self.props_to_html() + ">" + self.value + "</" + self.tag + ">"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode has no 'Tag'")
        if not self.children:
            raise ValueError("Parent has no 'Children'")
        string = ""
        for child in self.children:
            string = string+child.to_html()
        return "<" + self.tag + self.props_to_html() + ">" + string + "</" + self.tag + ">"