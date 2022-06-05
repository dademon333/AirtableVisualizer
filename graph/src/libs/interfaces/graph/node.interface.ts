import EntityType from "../../enums/entity-type.enum";

interface INode {
    id: string;
    name: string;
    x: number;
    y: number;
    connectedNodes: INode[];
    type: EntityType;
    text: string;
    radius: number;
}

export default INode;