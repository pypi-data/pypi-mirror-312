import { p as parser$1, f as flowDb } from "./flowDb-d35e309a-DG3-sY1h.js";
import { f as flowRendererV2, g as flowStyles } from "./styles-7383a064-CEbA9-ZW.js";
import { t as setConfig } from "./index-DVz7yIwd.js";
import "./graph-zXpYPmUz.js";
import "./layout-DASXMVg1.js";
import "./index-8fae9850-CeTLDNoy.js";
import "./clone-1VvyJIYC.js";
import "./edges-d417c7a0-sGI_aGLN.js";
import "./createText-423428c9-ByupGfrL.js";
import "./line-BNS5dJnk.js";
import "./array-DgktLKBx.js";
import "./path-Cp2qmpkd.js";
import "./channel-Bqox5XCE.js";
const diagram = {
  parser: parser$1,
  db: flowDb,
  renderer: flowRendererV2,
  styles: flowStyles,
  init: (cnf) => {
    if (!cnf.flowchart) {
      cnf.flowchart = {};
    }
    cnf.flowchart.arrowMarkerAbsolute = cnf.arrowMarkerAbsolute;
    setConfig({ flowchart: { arrowMarkerAbsolute: cnf.arrowMarkerAbsolute } });
    flowRendererV2.setConf(cnf.flowchart);
    flowDb.clear();
    flowDb.setGen("gen-2");
  }
};
export {
  diagram
};
//# sourceMappingURL=flowDiagram-v2-49332944-4ZFFiRXU.js.map
