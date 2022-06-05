import * as d3 from 'd3'
import INode from '../../interfaces/graph/node.interface';
import ILink from '../../interfaces/graph/nodes-link.interface';
import IEntitiesAndConnectionsResponse from "../../interfaces/response/entities-connections-response.interface";
import LinkModel from './link.model';
import NodeModel from './node.model';


class GraphModel {
    public nodes: INode[] = [];
    public links: ILink[] = [];

    private _width: number;
    private _height: number;
    private _svg: d3.Selection<SVGElement, unknown, HTMLElement, any>;
    private _svgElementName: string;
    private _nodeModel: NodeModel;
    private _linkModel: LinkModel;

    constructor(svgElementName: string, data: IEntitiesAndConnectionsResponse) {
        this._svgElementName = svgElementName;

        this._svg = d3.select("svg");
        this._width = Number(this._svg.attr("width"));
        this._height = Number(this._svg.attr("height"));

        this.initializeGraphNodes(data);
        this.initializeGraphLink(data);

        this._linkModel = new LinkModel(this._svgElementName, this.links);
        this._nodeModel = new NodeModel(this._svgElementName, this.nodes);
        

        this.addZooming();
    }

    public addSimulation(): void {
        const ticked = () => {
            this._linkModel.selection
              .attr("x1", d => d.source.x)
              .attr("y1", d => d.source.y)
              .attr("x2", d => d.target.x)
              .attr("y2", d => d.target.y);
        
            this._nodeModel.node
            .attr('transform', d => `translate(${d.x},${d.y})`);
          }

        const collideFormula = (radius: number) => radius > 5 ? (radius) / 25 + 15 : 25;
        const formula = (radius: number) =>  15 + radius / 5 + 5;

        d3.forceSimulation(this.nodes)
        .force('link', d3.forceLink(this.links).distance(d => getRandomArbitrary(200, 2000)))
        .force("charge", d3.forceManyBody().strength(-50))
        .force("center", d3.forceCenter(this._width / 2, this._height / 2))
        .force("collide", d3.forceCollide(d => formula(d.radius)))
        .on("tick", ticked.bind(this));
    }

    private initializeGraphNodes(data: IEntitiesAndConnectionsResponse): void {
        this.nodes = Object.entries(data.entities).map(entity => {
            const x = getRandomArbitrary(5, 5000);
            const y = getRandomArbitrary(5, 5000);
            const node: INode = {
                name: entity[1].name,
                x,
                y,
                id: entity[0],
                connectedNodes: [],
                type: entity[1].type,
                text: entity[1].name,
                radius: 15
            };

            return node;
        });
    }

    private initializeGraphLink(data: IEntitiesAndConnectionsResponse): void {
        for (const connection of data.connections) {
            for (const entityConnection of connection.entities_connections) {
                const source = this.nodes.find(node => node.id === entityConnection.parent_id.toString());
                const target = this.nodes.find(node => node.id === entityConnection.child_id.toString());
                if (!source || !target) {return;}
                source.radius++;
                source.connectedNodes.push(target);
                target.connectedNodes.push(source);

                const link: ILink = {
                    source, target
                };

                this.links.push(link);
            }
        }
    }

    private addZooming(): void {

        const zoomed = ({transform}: any) => {
            
            d3.selectAll("svg .nodes").attr("transform", transform);
            this._linkModel.selection.attr("transform", transform);
        }

        const zoom = d3.zoom<SVGElement, any>()
        .extent([[0, 0], [this._width, this._height]])
        .scaleExtent([1 , 10])
        .on("zoom", zoomed);

        zoom(this._svg);
    }
}

function getRandomArbitrary(min: number, max: number) {
    return Math.random() * (max - min) + min;
}

export default GraphModel;