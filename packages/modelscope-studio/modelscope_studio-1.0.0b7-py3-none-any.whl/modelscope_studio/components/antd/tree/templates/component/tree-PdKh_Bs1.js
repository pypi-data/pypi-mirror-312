import { g as le, w as L } from "./Index-d_LP_q09.js";
const E = window.ms_globals.React, te = window.ms_globals.React.forwardRef, ne = window.ms_globals.React.useRef, re = window.ms_globals.React.useState, oe = window.ms_globals.React.useEffect, V = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, A = window.ms_globals.antd.Tree;
var J = {
  exports: {}
}, S = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var se = E, ce = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ae = Object.prototype.hasOwnProperty, ue = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, de = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Y(e, t, r) {
  var o, l = {}, n = null, s = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) ae.call(t, o) && !de.hasOwnProperty(o) && (l[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: ce,
    type: e,
    key: n,
    ref: s,
    props: l,
    _owner: ue.current
  };
}
S.Fragment = ie;
S.jsx = Y;
S.jsxs = Y;
J.exports = S;
var p = J.exports;
const {
  SvelteComponent: fe,
  assign: W,
  binding_callbacks: M,
  check_outros: _e,
  children: K,
  claim_element: Q,
  claim_space: he,
  component_subscribe: U,
  compute_slots: me,
  create_slot: ge,
  detach: v,
  element: X,
  empty: z,
  exclude_internal_props: G,
  get_all_dirty_from_scope: we,
  get_slot_changes: pe,
  group_outros: be,
  init: ye,
  insert_hydration: k,
  safe_not_equal: Ee,
  set_custom_element_data: Z,
  space: ve,
  transition_in: j,
  transition_out: N,
  update_slot_base: Ie
} = window.__gradio__svelte__internal, {
  beforeUpdate: Re,
  getContext: xe,
  onDestroy: Ce,
  setContext: Oe
} = window.__gradio__svelte__internal;
function H(e) {
  let t, r;
  const o = (
    /*#slots*/
    e[7].default
  ), l = ge(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = X("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      t = Q(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = K(t);
      l && l.l(s), s.forEach(v), this.h();
    },
    h() {
      Z(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      k(n, t, s), l && l.m(t, null), e[9](t), r = !0;
    },
    p(n, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && Ie(
        l,
        o,
        n,
        /*$$scope*/
        n[6],
        r ? pe(
          o,
          /*$$scope*/
          n[6],
          s,
          null
        ) : we(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (j(l, n), r = !0);
    },
    o(n) {
      N(l, n), r = !1;
    },
    d(n) {
      n && v(t), l && l.d(n), e[9](null);
    }
  };
}
function Le(e) {
  let t, r, o, l, n = (
    /*$$slots*/
    e[4].default && H(e)
  );
  return {
    c() {
      t = X("react-portal-target"), r = ve(), n && n.c(), o = z(), this.h();
    },
    l(s) {
      t = Q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(t).forEach(v), r = he(s), n && n.l(s), o = z(), this.h();
    },
    h() {
      Z(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      k(s, t, c), e[8](t), k(s, r, c), n && n.m(s, c), k(s, o, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, c), c & /*$$slots*/
      16 && j(n, 1)) : (n = H(s), n.c(), j(n, 1), n.m(o.parentNode, o)) : n && (be(), N(n, 1, 1, () => {
        n = null;
      }), _e());
    },
    i(s) {
      l || (j(n), l = !0);
    },
    o(s) {
      N(n), l = !1;
    },
    d(s) {
      s && (v(t), v(r), v(o)), e[8](null), n && n.d(s);
    }
  };
}
function q(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function ke(e, t, r) {
  let o, l, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const c = me(n);
  let {
    svelteInit: i
  } = t;
  const m = L(q(t)), u = L();
  U(e, u, (d) => r(0, o = d));
  const f = L();
  U(e, f, (d) => r(1, l = d));
  const a = [], h = xe("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: g,
    subSlotIndex: w
  } = le() || {}, y = i({
    parent: h,
    props: m,
    target: u,
    slot: f,
    slotKey: _,
    slotIndex: g,
    subSlotIndex: w,
    onDestroy(d) {
      a.push(d);
    }
  });
  Oe("$$ms-gr-react-wrapper", y), Re(() => {
    m.set(q(t));
  }), Ce(() => {
    a.forEach((d) => d());
  });
  function b(d) {
    M[d ? "unshift" : "push"](() => {
      o = d, u.set(o);
    });
  }
  function P(d) {
    M[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  return e.$$set = (d) => {
    r(17, t = W(W({}, t), G(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, t = G(t), [o, l, u, f, c, i, s, n, b, P];
}
class je extends fe {
  constructor(t) {
    super(), ye(this, t, ke, Le, Ee, {
      svelteInit: 5
    });
  }
}
const B = window.ms_globals.rerender, T = window.ms_globals.tree;
function Se(e) {
  function t(r) {
    const o = L(), l = new je({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, c = n.parent ?? T;
          return c.nodes = [...c.nodes, s], B({
            createPortal: F,
            node: T
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), B({
              createPortal: F,
              node: T
            });
          }), s;
        },
        ...r.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Te(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const o = e[r];
    return typeof o == "number" && !Pe.includes(r) ? t[r] = o + "px" : t[r] = o, t;
  }, {}) : {};
}
function D(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(F(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((l) => {
        if (E.isValidElement(l) && l.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = D(l.props.el);
          return E.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...E.Children.toArray(l.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((l) => {
    e.getEventListeners(l).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const o = Array.from(e.childNodes);
  for (let l = 0; l < o.length; l++) {
    const n = o[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = D(n);
      t.push(...c), r.appendChild(s);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Fe(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const C = te(({
  slot: e,
  clone: t,
  className: r,
  style: o
}, l) => {
  const n = ne(), [s, c] = re([]);
  return oe(() => {
    var f;
    if (!n.current || !e)
      return;
    let i = e;
    function m() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Fe(l, a), r && a.classList.add(...r.split(" ")), o) {
        const h = Te(o);
        Object.keys(h).forEach((_) => {
          a.style[_] = h[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var w, y, b;
        (w = n.current) != null && w.contains(i) && ((y = n.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: g
        } = D(e);
        return i = g, c(_), i.style.display = "contents", m(), (b = n.current) == null || b.appendChild(i), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", m(), (f = n.current) == null || f.appendChild(i);
    return () => {
      var a, h;
      i.style.display = "", (a = n.current) != null && a.contains(i) && ((h = n.current) == null || h.removeChild(i)), u == null || u.disconnect();
    };
  }, [e, t, r, o, l]), E.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ne(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function De(e, t = !1) {
  try {
    if (t && !Ne(e))
      return;
    if (typeof e == "string") {
      let r = e.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function x(e, t) {
  return V(() => De(e, t), [e, t]);
}
function Ae(e) {
  return Object.keys(e).reduce((t, r) => (e[r] !== void 0 && (t[r] = e[r]), t), {});
}
function $(e, t, r) {
  return e.filter(Boolean).map((o, l) => {
    var i;
    if (typeof o != "object")
      return t != null && t.fallback ? t.fallback(o) : o;
    const n = {
      ...o.props,
      key: ((i = o.props) == null ? void 0 : i.key) ?? (r ? `${r}-${l}` : `${l}`)
    };
    let s = n;
    Object.keys(o.slots).forEach((m) => {
      if (!o.slots[m] || !(o.slots[m] instanceof Element) && !o.slots[m].el)
        return;
      const u = m.split(".");
      u.forEach((g, w) => {
        s[g] || (s[g] = {}), w !== u.length - 1 && (s = n[g]);
      });
      const f = o.slots[m];
      let a, h, _ = (t == null ? void 0 : t.clone) ?? !1;
      f instanceof Element ? a = f : (a = f.el, h = f.callback, _ = f.clone ?? !1), s[u[u.length - 1]] = a ? h ? (...g) => (h(u[u.length - 1], g), /* @__PURE__ */ p.jsx(C, {
        slot: a,
        clone: _
      })) : /* @__PURE__ */ p.jsx(C, {
        slot: a,
        clone: _
      }) : s[u[u.length - 1]], s = n;
    });
    const c = (t == null ? void 0 : t.children) || "children";
    return o[c] && (n[c] = $(o[c], t, `${l}`)), n;
  });
}
function We(e, t) {
  return e ? /* @__PURE__ */ p.jsx(C, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function O({
  key: e,
  setSlotParams: t,
  slots: r
}, o) {
  return r[e] ? (...l) => (t(e, l), We(r[e], {
    clone: !0,
    ...o
  })) : void 0;
}
const Ue = Se(({
  slots: e,
  filterTreeNode: t,
  treeData: r,
  draggable: o,
  allowDrop: l,
  onCheck: n,
  onSelect: s,
  onExpand: c,
  children: i,
  directory: m,
  slotItems: u,
  setSlotParams: f,
  onLoadData: a,
  titleRender: h,
  ..._
}) => {
  const g = x(t), w = x(o), y = x(h), b = x(typeof o == "object" ? o.nodeDraggable : void 0), P = x(l), d = m ? A.DirectoryTree : A, ee = V(() => ({
    ..._,
    treeData: r || $(u, {
      clone: !0
    }),
    showLine: e["showLine.showLeafIcon"] ? {
      showLeafIcon: O({
        slots: e,
        setSlotParams: f,
        key: "showLine.showLeafIcon"
      })
    } : _.showLine,
    icon: e.icon ? O({
      slots: e,
      setSlotParams: f,
      key: "icon"
    }) : _.icon,
    switcherLoadingIcon: e.switcherLoadingIcon ? /* @__PURE__ */ p.jsx(C, {
      slot: e.switcherLoadingIcon
    }) : _.switcherLoadingIcon,
    switcherIcon: e.switcherIcon ? O({
      slots: e,
      setSlotParams: f,
      key: "switcherIcon"
    }) : _.switcherIcon,
    titleRender: e.titleRender ? O({
      slots: e,
      setSlotParams: f,
      key: "titleRender"
    }) : y,
    draggable: e["draggable.icon"] || b ? {
      icon: e["draggable.icon"] ? /* @__PURE__ */ p.jsx(C, {
        slot: e["draggable.icon"]
      }) : typeof o == "object" ? o.icon : void 0,
      nodeDraggable: b
    } : w || o,
    loadData: a
  }), [_, r, u, e, f, b, o, y, w, a]);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: i
    }), /* @__PURE__ */ p.jsx(d, {
      ...Ae(ee),
      filterTreeNode: g,
      allowDrop: P,
      onSelect: (I, ...R) => {
        s == null || s(I, ...R);
      },
      onExpand: (I, ...R) => {
        c == null || c(I, ...R);
      },
      onCheck: (I, ...R) => {
        n == null || n(I, ...R);
      }
    })]
  });
});
export {
  Ue as Tree,
  Ue as default
};
