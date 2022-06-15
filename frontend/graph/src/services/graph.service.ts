import INode from "../interfaces/graph/node.interface";
import ILink from "../interfaces/graph/nodes-link.interface";
import { IVisibleEntity } from "../redux/slices/filter.slice";
import { getVisibleNodes as visibleNodes } from "./event.service";

export function getVisibleNodes(): IVisibleEntity[] {
    const visibleEntities: IVisibleEntity[] = [];
    document.querySelectorAll('.node').forEach(el => {
        const opacity = el.getAttribute('opacity');
        if (opacity === '1') {
            const name = el.getAttribute('name')!;
            const id = el.getAttribute('id')!;
            visibleEntities.push({name, id})
        }
    });

    return visibleEntities;
}

export type PathFindingNode = INode & {visited: boolean, distance: number};

export function getShortestPath(from: string, to: string): PathFindingNode | null {
    let startNode: PathFindingNode;
    const distances: {[id: string]: PathFindingNode} = {};
    const nodes = visibleNodes();
    console.log(nodes);

    const f = (node: INode) => {
        const pathFindingNode: PathFindingNode = {
            ...node,
            visited: node.id === from,
            distance: node.id === from ? 0 : Number.MAX_VALUE,
        };

        if (pathFindingNode.visited) {
            startNode = pathFindingNode;
        }
        
        distances[node.id] = pathFindingNode;
    }

    nodes.forEach(el => {
        f(el);
        el.connectedNodes.forEach(cn => f(cn));

      });

      visitNodesRecursivly(startNode!, distances);
      if (distances[to].distance === Number.MAX_VALUE) {
          return null;
      }
  
      const el = distances[to];
      return el;
    }

const visitNodesRecursivly = (currentNode: PathFindingNode, distances: {[id: string]: PathFindingNode}) => {

    const paths = currentNode.connectedNodes;
    for (const connectedNode of paths) {
        const distanceToCity = currentNode.distance + 1;
        if (distanceToCity < distances[connectedNode.id].distance) {
            distances[connectedNode.id].distance = distanceToCity;
        }

        if (distances[connectedNode.id].visited) continue;

        distances[connectedNode.id].visited = true;
        visitNodesRecursivly(distances[connectedNode.id], distances);
    }
}