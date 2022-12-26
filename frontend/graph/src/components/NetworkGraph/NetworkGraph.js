import { useEffect, useState } from 'react'
import { Graph } from "react-d3-graph";
import "./NetworkGraph.css"
import { useSelector } from 'react-redux';

const NetworkGraph = ({data}) => {

  const [graphData, setGraphData] = useState({
    nodes: [{ id: "Node 1" }, { id: "Node 2" }, { id: "Node 3" }],
    links: [
    { source: "Node 1", target: "Node 2", label: "label"},
    { source: "Node 1", target: "Node 3" },
  ]})

  const selectFilters = useSelector(state => state.filters)
  
  const formatData = (rawData) => {
   return {
    nodes: rawData.entities
    .filter(entity => selectFilters.components.types.length ? selectFilters.components.types.includes(entity.type) : entity)
    .map(entity => ({id: entity.id, name: entity.name, type: entity.type})),
    links: rawData.connections
    .filter(link => selectFilters.components.types.length ? selectFilters.components.types.includes(rawData.entities.find(entity => entity.id == link.parent_id).type) && selectFilters.components.types.includes(rawData.entities.find(entity => entity.id == link.child_id).type) : link)
    .map(link => ({source: link.parent_id, target: link.child_id}))
  }
}
  useEffect(() => {
    setGraphData(formatData(data))
    console.log(graphData)
  },[selectFilters])

  const lightData = {
    nodes: [{ id: "Node 1" }, { id: "Node 2" }, { id: "Node 3" }],
    links: [
    { source: "Node 1", target: "Node 2", label: "label"},
    { source: "Node 1", target: "Node 3" },
  ]}
  

  const [windowDimensions, setWindowDimensions] = useState({width: window.innerWidth, height: window.innerHeight});
  useEffect(() => {
    function handleResize() {
      
      setWindowDimensions({width: window.innerWidth, height: window.innerHeight});
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

const myConfig = {
  automaticRearrangeAfterDropNode: true,
  directed: true,
  nodeHighlightBehavior: true,
  width: windowDimensions.width - 415,
  height: windowDimensions.height - 30,
  d3: {
    alphaTarget: 0.6,
    gravity: -300,
    linkLength: 50,
    linkStrength: 20,
  },
  node: {
    fontWeight: 300,
    fontSize: 8,
    labelPosition: "bottom",
    labelProperty: 'name',
    color: "lightgreen",
    size: 468,
    highlightStrokeColor: "blue",
    highlightFontSize: 15
    
  },
  link: {
    type: "STRAIGHT",
    highlightColor: "lightblue",
    labelProperty: "label",
    renderLabel: true,
    fontSize: 15,
  },
};

const onClickNode = function(nodeId) {
  window.alert(`Clicked node ${nodeId}`);
};

const onClickLink = function(source, target) {
  window.alert(`Clicked link between ${source} and ${target}`);
};

const onClickGraph = function(e) {
  console.log(e);
}
  return (
    <div className="network-graph">
        <Graph
            id="graph-id" 
            data={graphData}
            config={myConfig}
            // onClickNode={onClickNode}
            // onClickLink={onClickLink}
            // onClickGraph={onClickGraph}
        />
    </div>
  )
}

export default NetworkGraph
