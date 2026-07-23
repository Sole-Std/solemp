use godot::prelude::*;

#[derive(GodotClass)]
#[class(base=Node)]
struct NetworkEntity {
    base: Base<Node>
}

#[godot_api]
impl INode for NetworkEntity {
    fn init(base: Base<Node>) -> Self {
        godot_print!("Hello World");

        Self { base }
    }
}