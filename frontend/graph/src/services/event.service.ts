import { Observable, Subject } from "rxjs";
import INode from "../interfaces/graph/node.interface";
import { IVisibleEntity } from "../redux/slices/filter.slice";
import { getVisibleNodes as getGraphVisibleNodes } from "./graph.service";

const _onTransformToElement: Subject<string> = new Subject<string>();
const _onVisibleNodesChange: Subject<IVisibleEntity[]> = new Subject<IVisibleEntity[]>();
let _visibleNodes: INode[] = [];

export function onTransformToElement(): Observable<string> {
    return _onTransformToElement.asObservable();
}

export function transformToElement(id: string): void {
    _onTransformToElement.next(id);
}

export function onVisibleNodesChange(): Observable<IVisibleEntity[]> {
    return _onVisibleNodesChange.asObservable();
}

export function visibleNodesChanged(): void {
    const visibleNodes = getGraphVisibleNodes();
    _onVisibleNodesChange.next(visibleNodes);
}

export function setVisibleNodes(nodes: INode[]): void {_visibleNodes = nodes; }
export function getVisibleNodes(): INode[] {return _visibleNodes; }
