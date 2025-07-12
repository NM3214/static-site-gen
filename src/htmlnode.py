class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        props_string = ""
        if self.props:
            for key, value in self.props.items():
                props_string += (f' {key}="{value}"')
        return props_string


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node has no value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Error with ParentNode.to_html(): No tag")
        if not self.children:
            raise ValueError("Error with ParentNode.to_html(): No children")
        children_to_html = ""
        for child in self.children:
            children_to_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_to_html}</{self.tag}>"