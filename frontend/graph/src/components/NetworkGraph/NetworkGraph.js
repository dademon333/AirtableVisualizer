import { useEffect, useState } from 'react'
import { Graph } from "react-d3-graph";
import GraphComponent from './graphComponent/GraphComponent';
import "./NetworkGraph.css"
import { useSelector } from 'react-redux';
import { getEntityColor } from '../../services/entity.serivce';

const NetworkGraph = ({data}) => {
  
  const [updateKey, setUpdateKey] = useState(0);
  const [graphData, setGraphData] = useState({
    nodes: [],
    links: []})

  const selectFilters = useSelector(state => state.filters)
  
  const formatData = (rawData) => {
    return selectFilters.components.types.length ? {
    nodes: rawData.entities
    .filter(entity => selectFilters.components.types.length ? selectFilters.components.types.includes(entity.type) : entity)
    .map(entity => ({id: entity.id, name: entity.name, type: entity.type, color: getEntityColor(entity.type)})),
    links: rawData.connections
    .filter(link => selectFilters.components.types.length ? selectFilters.components.types.includes(rawData.entities.find(entity => entity.id == link.parent_id).type) && selectFilters.components.types.includes(rawData.entities.find(entity => entity.id == link.child_id).type) : link)
    .map(link => ({source: link.parent_id, target: link.child_id, color: getEntityColor(rawData.entities.find(entity => entity.id == link.parent_id).type)}))
  } : {nodes: [], links: []}
}

  useEffect(() => {
    setGraphData(createRoot(formatData(data)))
    console.log(createRoot(formatData(data)))

  },[selectFilters])


  const createRoot = (newData) => {
    newData.nodes.push({id: 'root',name: 'вершины без связи', opacity: '0'})
    newData.nodes.filter(node => !(node.id == 'root' || newData.links.map(link => [link.target, link.source]).flat(1).includes(node.id))).forEach(node => newData.links.push({source: 'root', target: node.id, opacity: '0', hihglightOpacity: '0'}))
    return(newData)
  }

  useEffect(() => {
    if (graphData.nodes.length) {
      setUpdateKey((k) => ++k);
    }
  }, [graphData]);

  

  const [windowDimensions, setWindowDimensions] = useState({width: window.innerWidth, height: window.innerHeight});
  useEffect(() => {
    function handleResize() {
      
      setWindowDimensions({width: window.innerWidth, height: window.innerHeight});
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

const myConfig = {
  // automaticRearrangeAfterDropNode: true,
  directed: true,
  nodeHighlightBehavior: true,
  width: windowDimensions.width - 415,
  height: windowDimensions.height - 30,
  d3: {
    alphaTarget: 1,
    gravity: -300,
    linkLength: 100,
    linkStrength: 1,
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
    color: "000000",
    type: "CURVE_SMOOTH",
    highlightColor: "SAME",
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
    <div className="network-graph" key={updateKey}>
        <GraphComponent
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
