import ReactFlow, { Background, Controls } from "reactflow";
import "reactflow/dist/style.css";

function DependencyGraph({ analysis }) {
  const dependencies = analysis.dependencies || [];
  const serviceCounts = analysis.serviceCounts || {};

  const services = Array.from(
    new Set(dependencies.flatMap((edge) => [edge.source, edge.target]))
  );

  const nodes = services.map((service, index) => {
    const count = serviceCounts[service] || 0;

    let background = "#064e3b";

    if (count >= 3) {
      background = "#7f1d1d";
    } else if (count >= 2) {
      background = "#78350f";
    }

    return {
      id: service,
      position: {
        x: (index % 3) * 260,
        y: Math.floor(index / 3) * 160,
      },
      data: {
        label: `${service} (${count})`,
      },
      style: {
        background,
        color: "#e5e7eb",
        border: "1px solid #334155",
        borderRadius: 12,
        padding: 12,
        fontWeight: "bold",
      },
    };
  });

  const edges = dependencies.map((edge, index) => ({
    id: `${edge.source}-${edge.target}-${index}`,
    source: edge.source,
    target: edge.target,
    animated: true,
    label: "possible cascade",
  }));

  return (
    <div style={{ height: 350 }}>
      <ReactFlow nodes={nodes} edges={edges} fitView>
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
}

export default DependencyGraph;