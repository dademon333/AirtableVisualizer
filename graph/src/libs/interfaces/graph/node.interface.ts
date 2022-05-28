import EntityType from "../../enums/entity-type.enum";

interface INode {
    id: string;
    name: string;
    x: number;
    y: number;
    connectedNodesCount: number;
    type: EntityType;
    text: string;
}

export default INode;