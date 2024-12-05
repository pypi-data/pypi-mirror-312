import { g as Oe, w as I } from "./Index-CR3xJeXj.js";
const y = window.ms_globals.React, Ce = window.ms_globals.React.forwardRef, be = window.ms_globals.React.useRef, ye = window.ms_globals.React.useState, Ee = window.ms_globals.React.useEffect, L = window.ms_globals.React.useMemo, W = window.ms_globals.ReactDOM.createPortal, k = window.ms_globals.antd.Table;
var Z = {
  exports: {}
}, M = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ve = y, Re = Symbol.for("react.element"), Se = Symbol.for("react.fragment"), ke = Object.prototype.hasOwnProperty, xe = ve.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function $(n, e, r) {
  var o, l = {}, t = null, i = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (i = e.ref);
  for (o in e) ke.call(e, o) && !Ne.hasOwnProperty(o) && (l[o] = e[o]);
  if (n && n.defaultProps) for (o in e = n.defaultProps, e) l[o] === void 0 && (l[o] = e[o]);
  return {
    $$typeof: Re,
    type: n,
    key: t,
    ref: i,
    props: l,
    _owner: xe.current
  };
}
M.Fragment = Se;
M.jsx = $;
M.jsxs = $;
Z.exports = M;
var w = Z.exports;
const {
  SvelteComponent: Pe,
  assign: H,
  binding_callbacks: Q,
  check_outros: Te,
  children: ee,
  claim_element: te,
  claim_space: Le,
  component_subscribe: z,
  compute_slots: Ie,
  create_slot: je,
  detach: S,
  element: ne,
  empty: X,
  exclude_internal_props: q,
  get_all_dirty_from_scope: Fe,
  get_slot_changes: Ae,
  group_outros: Me,
  init: Ue,
  insert_hydration: j,
  safe_not_equal: De,
  set_custom_element_data: re,
  space: We,
  transition_in: F,
  transition_out: B,
  update_slot_base: Be
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ge,
  getContext: Je,
  onDestroy: He,
  setContext: Qe
} = window.__gradio__svelte__internal;
function V(n) {
  let e, r;
  const o = (
    /*#slots*/
    n[7].default
  ), l = je(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = ne("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      e = te(t, "SVELTE-SLOT", {
        class: !0
      });
      var i = ee(e);
      l && l.l(i), i.forEach(S), this.h();
    },
    h() {
      re(e, "class", "svelte-1rt0kpf");
    },
    m(t, i) {
      j(t, e, i), l && l.m(e, null), n[9](e), r = !0;
    },
    p(t, i) {
      l && l.p && (!r || i & /*$$scope*/
      64) && Be(
        l,
        o,
        t,
        /*$$scope*/
        t[6],
        r ? Ae(
          o,
          /*$$scope*/
          t[6],
          i,
          null
        ) : Fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (F(l, t), r = !0);
    },
    o(t) {
      B(l, t), r = !1;
    },
    d(t) {
      t && S(e), l && l.d(t), n[9](null);
    }
  };
}
function ze(n) {
  let e, r, o, l, t = (
    /*$$slots*/
    n[4].default && V(n)
  );
  return {
    c() {
      e = ne("react-portal-target"), r = We(), t && t.c(), o = X(), this.h();
    },
    l(i) {
      e = te(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), ee(e).forEach(S), r = Le(i), t && t.l(i), o = X(), this.h();
    },
    h() {
      re(e, "class", "svelte-1rt0kpf");
    },
    m(i, c) {
      j(i, e, c), n[8](e), j(i, r, c), t && t.m(i, c), j(i, o, c), l = !0;
    },
    p(i, [c]) {
      /*$$slots*/
      i[4].default ? t ? (t.p(i, c), c & /*$$slots*/
      16 && F(t, 1)) : (t = V(i), t.c(), F(t, 1), t.m(o.parentNode, o)) : t && (Me(), B(t, 1, 1, () => {
        t = null;
      }), Te());
    },
    i(i) {
      l || (F(t), l = !0);
    },
    o(i) {
      B(t), l = !1;
    },
    d(i) {
      i && (S(e), S(r), S(o)), n[8](null), t && t.d(i);
    }
  };
}
function K(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function Xe(n, e, r) {
  let o, l, {
    $$slots: t = {},
    $$scope: i
  } = e;
  const c = Ie(t);
  let {
    svelteInit: s
  } = e;
  const g = I(K(e)), u = I();
  z(n, u, (f) => r(0, o = f));
  const d = I();
  z(n, d, (f) => r(1, l = f));
  const a = [], _ = Je("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: h,
    subSlotIndex: C
  } = Oe() || {}, O = s({
    parent: _,
    props: g,
    target: u,
    slot: d,
    slotKey: p,
    slotIndex: h,
    subSlotIndex: C,
    onDestroy(f) {
      a.push(f);
    }
  });
  Qe("$$ms-gr-react-wrapper", O), Ge(() => {
    g.set(K(e));
  }), He(() => {
    a.forEach((f) => f());
  });
  function v(f) {
    Q[f ? "unshift" : "push"](() => {
      o = f, u.set(o);
    });
  }
  function R(f) {
    Q[f ? "unshift" : "push"](() => {
      l = f, d.set(l);
    });
  }
  return n.$$set = (f) => {
    r(17, e = H(H({}, e), q(f))), "svelteInit" in f && r(5, s = f.svelteInit), "$$scope" in f && r(6, i = f.$$scope);
  }, e = q(e), [o, l, u, d, c, s, i, t, v, R];
}
class qe extends Pe {
  constructor(e) {
    super(), Ue(this, e, Xe, ze, De, {
      svelteInit: 5
    });
  }
}
const Y = window.ms_globals.rerender, D = window.ms_globals.tree;
function Ve(n) {
  function e(r) {
    const o = I(), l = new qe({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? D;
          return c.nodes = [...c.nodes, i], Y({
            createPortal: W,
            node: D
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((s) => s.svelteInstance !== o), Y({
              createPortal: W,
              node: D
            });
          }), i;
        },
        ...r.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(e);
    });
  });
}
const Ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ye(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const o = n[r];
    return typeof o == "number" && !Ke.includes(r) ? e[r] = o + "px" : e[r] = o, e;
  }, {}) : {};
}
function G(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(W(y.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: y.Children.toArray(n._reactElement.props.children).map((l) => {
        if (y.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: i
          } = G(l.props.el);
          return y.cloneElement(l, {
            ...l.props,
            el: i,
            children: [...y.Children.toArray(l.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((l) => {
    n.getEventListeners(l).forEach(({
      listener: i,
      type: c,
      useCapture: s
    }) => {
      r.addEventListener(c, i, s);
    });
  });
  const o = Array.from(n.childNodes);
  for (let l = 0; l < o.length; l++) {
    const t = o[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: i,
        portals: c
      } = G(t);
      e.push(...c), r.appendChild(i);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Ze(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const E = Ce(({
  slot: n,
  clone: e,
  className: r,
  style: o
}, l) => {
  const t = be(), [i, c] = ye([]);
  return Ee(() => {
    var d;
    if (!t.current || !n)
      return;
    let s = n;
    function g() {
      let a = s;
      if (s.tagName.toLowerCase() === "svelte-slot" && s.children.length === 1 && s.children[0] && (a = s.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ze(l, a), r && a.classList.add(...r.split(" ")), o) {
        const _ = Ye(o);
        Object.keys(_).forEach((p) => {
          a.style[p] = _[p];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var C, O, v;
        (C = t.current) != null && C.contains(s) && ((O = t.current) == null || O.removeChild(s));
        const {
          portals: p,
          clonedElement: h
        } = G(n);
        return s = h, c(p), s.style.display = "contents", g(), (v = t.current) == null || v.appendChild(s), p.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      s.style.display = "contents", g(), (d = t.current) == null || d.appendChild(s);
    return () => {
      var a, _;
      s.style.display = "", (a = t.current) != null && a.contains(s) && ((_ = t.current) == null || _.removeChild(s)), u == null || u.disconnect();
    };
  }, [n, e, r, o, l]), y.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...i);
});
function $e(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function et(n, e = !1) {
  try {
    if (e && !$e(n))
      return;
    if (typeof n == "string") {
      let r = n.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function m(n, e) {
  return L(() => et(n, e), [n, e]);
}
function tt(n) {
  return Object.keys(n).reduce((e, r) => (n[r] !== void 0 && (e[r] = n[r]), e), {});
}
function A(n, e, r) {
  return n.filter(Boolean).map((o, l) => {
    var s;
    if (typeof o != "object")
      return e != null && e.fallback ? e.fallback(o) : o;
    const t = {
      ...o.props,
      key: ((s = o.props) == null ? void 0 : s.key) ?? (r ? `${r}-${l}` : `${l}`)
    };
    let i = t;
    Object.keys(o.slots).forEach((g) => {
      if (!o.slots[g] || !(o.slots[g] instanceof Element) && !o.slots[g].el)
        return;
      const u = g.split(".");
      u.forEach((h, C) => {
        i[h] || (i[h] = {}), C !== u.length - 1 && (i = t[h]);
      });
      const d = o.slots[g];
      let a, _, p = (e == null ? void 0 : e.clone) ?? !1;
      d instanceof Element ? a = d : (a = d.el, _ = d.callback, p = d.clone ?? !1), i[u[u.length - 1]] = a ? _ ? (...h) => (_(u[u.length - 1], h), /* @__PURE__ */ w.jsx(E, {
        slot: a,
        clone: p
      })) : /* @__PURE__ */ w.jsx(E, {
        slot: a,
        clone: p
      }) : i[u[u.length - 1]], i = t;
    });
    const c = (e == null ? void 0 : e.children) || "children";
    return o[c] && (t[c] = A(o[c], e, `${l}`)), t;
  });
}
function nt(n, e) {
  return n ? /* @__PURE__ */ w.jsx(E, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function P({
  key: n,
  setSlotParams: e,
  slots: r
}, o) {
  return r[n] ? (...l) => (e(n, l), nt(r[n], {
    clone: !0,
    ...o
  })) : void 0;
}
function T(n) {
  return typeof n == "object" && n !== null ? n : {};
}
const ot = Ve(({
  children: n,
  slots: e,
  columnItems: r,
  columns: o,
  getPopupContainer: l,
  pagination: t,
  loading: i,
  rowKey: c,
  rowClassName: s,
  summary: g,
  rowSelection: u,
  rowSelectionItems: d,
  expandableItems: a,
  expandable: _,
  sticky: p,
  footer: h,
  showSorterTooltip: C,
  onRow: O,
  onHeaderRow: v,
  setSlotParams: R,
  ...f
}) => {
  const oe = m(l), le = e["loading.tip"] || e["loading.indicator"], U = T(i), ie = e["pagination.showQuickJumper.goButton"] || e["pagination.itemRender"], x = T(t), se = m(x.showTotal), ce = m(s), ae = m(c), ue = e["showSorterTooltip.title"] || typeof C == "object", N = T(C), fe = m(N.afterOpenChange), de = m(N.getPopupContainer), pe = typeof p == "object", J = T(p), _e = m(J.getContainer), ge = m(O), he = m(v), me = m(g), we = m(h);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ w.jsx(k, {
      ...f,
      columns: L(() => (o == null ? void 0 : o.map((b) => b === "EXPAND_COLUMN" ? k.EXPAND_COLUMN : b === "SELECTION_COLUMN" ? k.SELECTION_COLUMN : b)) || A(r, {
        fallback: (b) => b === "EXPAND_COLUMN" ? k.EXPAND_COLUMN : b === "SELECTION_COLUMN" ? k.SELECTION_COLUMN : b
      }), [r, o]),
      onRow: ge,
      onHeaderRow: he,
      summary: e.summary ? P({
        slots: e,
        setSlotParams: R,
        key: "summary"
      }) : me,
      rowSelection: L(() => u || A(d)[0], [u, d]),
      expandable: L(() => _ || A(a)[0], [_, a]),
      rowClassName: ce,
      rowKey: ae || c,
      sticky: pe ? {
        ...J,
        getContainer: _e
      } : p,
      showSorterTooltip: ue ? {
        ...N,
        afterOpenChange: fe,
        getPopupContainer: de,
        title: e["showSorterTooltip.title"] ? /* @__PURE__ */ w.jsx(E, {
          slot: e["showSorterTooltip.title"]
        }) : N.title
      } : C,
      pagination: ie ? tt({
        ...x,
        showTotal: se,
        showQuickJumper: e["pagination.showQuickJumper.goButton"] ? {
          goButton: /* @__PURE__ */ w.jsx(E, {
            slot: e["pagination.showQuickJumper.goButton"]
          })
        } : x.showQuickJumper,
        itemRender: e["pagination.itemRender"] ? P({
          slots: e,
          setSlotParams: R,
          key: "pagination.itemRender"
        }) : x.itemRender
      }) : t,
      getPopupContainer: oe,
      loading: le ? {
        ...U,
        tip: e["loading.tip"] ? /* @__PURE__ */ w.jsx(E, {
          slot: e["loading.tip"]
        }) : U.tip,
        indicator: e["loading.indicator"] ? /* @__PURE__ */ w.jsx(E, {
          slot: e["loading.indicator"]
        }) : U.indicator
      } : i,
      footer: e.footer ? P({
        slots: e,
        setSlotParams: R,
        key: "footer"
      }) : we,
      title: e.title ? P({
        slots: e,
        setSlotParams: R,
        key: "title"
      }) : f.title
    })]
  });
});
export {
  ot as Table,
  ot as default
};
