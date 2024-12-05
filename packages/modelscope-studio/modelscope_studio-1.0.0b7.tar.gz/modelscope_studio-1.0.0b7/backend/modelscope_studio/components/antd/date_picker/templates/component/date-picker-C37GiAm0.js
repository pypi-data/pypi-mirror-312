import { g as be, w as P } from "./Index-BxHAkNOD.js";
const I = window.ms_globals.React, he = window.ms_globals.React.forwardRef, ve = window.ms_globals.React.useRef, ge = window.ms_globals.React.useState, we = window.ms_globals.React.useEffect, g = window.ms_globals.React.useMemo, M = window.ms_globals.ReactDOM.createPortal, ye = window.ms_globals.antd.DatePicker, z = window.ms_globals.dayjs;
var X = {
  exports: {}
}, N = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var xe = I, Ee = Symbol.for("react.element"), Ie = Symbol.for("react.fragment"), Re = Object.prototype.hasOwnProperty, Ce = xe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, je = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Z(e, n, r) {
  var o, l = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (o in n) Re.call(n, o) && !je.hasOwnProperty(o) && (l[o] = n[o]);
  if (e && e.defaultProps) for (o in n = e.defaultProps, n) l[o] === void 0 && (l[o] = n[o]);
  return {
    $$typeof: Ee,
    type: e,
    key: t,
    ref: s,
    props: l,
    _owner: Ce.current
  };
}
N.Fragment = Ie;
N.jsx = Z;
N.jsxs = Z;
X.exports = N;
var h = X.exports;
const {
  SvelteComponent: Se,
  assign: G,
  binding_callbacks: U,
  check_outros: ke,
  children: $,
  claim_element: ee,
  claim_space: Oe,
  component_subscribe: H,
  compute_slots: Pe,
  create_slot: Fe,
  detach: j,
  element: te,
  empty: q,
  exclude_internal_props: B,
  get_all_dirty_from_scope: De,
  get_slot_changes: Ne,
  group_outros: Ae,
  init: Le,
  insert_hydration: F,
  safe_not_equal: Te,
  set_custom_element_data: ne,
  space: Me,
  transition_in: D,
  transition_out: W,
  update_slot_base: We
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ve,
  getContext: ze,
  onDestroy: Ge,
  setContext: Ue
} = window.__gradio__svelte__internal;
function J(e) {
  let n, r;
  const o = (
    /*#slots*/
    e[7].default
  ), l = Fe(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = te("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      n = ee(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = $(n);
      l && l.l(s), s.forEach(j), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      F(t, n, s), l && l.m(n, null), e[9](n), r = !0;
    },
    p(t, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && We(
        l,
        o,
        t,
        /*$$scope*/
        t[6],
        r ? Ne(
          o,
          /*$$scope*/
          t[6],
          s,
          null
        ) : De(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (D(l, t), r = !0);
    },
    o(t) {
      W(l, t), r = !1;
    },
    d(t) {
      t && j(n), l && l.d(t), e[9](null);
    }
  };
}
function He(e) {
  let n, r, o, l, t = (
    /*$$slots*/
    e[4].default && J(e)
  );
  return {
    c() {
      n = te("react-portal-target"), r = Me(), t && t.c(), o = q(), this.h();
    },
    l(s) {
      n = ee(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), $(n).forEach(j), r = Oe(s), t && t.l(s), o = q(), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      F(s, n, c), e[8](n), F(s, r, c), t && t.m(s, c), F(s, o, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && D(t, 1)) : (t = J(s), t.c(), D(t, 1), t.m(o.parentNode, o)) : t && (Ae(), W(t, 1, 1, () => {
        t = null;
      }), ke());
    },
    i(s) {
      l || (D(t), l = !0);
    },
    o(s) {
      W(t), l = !1;
    },
    d(s) {
      s && (j(n), j(r), j(o)), e[8](null), t && t.d(s);
    }
  };
}
function Y(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function qe(e, n, r) {
  let o, l, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const c = Pe(t);
  let {
    svelteInit: i
  } = n;
  const p = P(Y(n)), u = P();
  H(e, u, (d) => r(0, o = d));
  const f = P();
  H(e, f, (d) => r(1, l = d));
  const a = [], _ = ze("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: v,
    subSlotIndex: y
  } = be() || {}, x = i({
    parent: _,
    props: p,
    target: u,
    slot: f,
    slotKey: m,
    slotIndex: v,
    subSlotIndex: y,
    onDestroy(d) {
      a.push(d);
    }
  });
  Ue("$$ms-gr-react-wrapper", x), Ve(() => {
    p.set(Y(n));
  }), Ge(() => {
    a.forEach((d) => d());
  });
  function R(d) {
    U[d ? "unshift" : "push"](() => {
      o = d, u.set(o);
    });
  }
  function S(d) {
    U[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  return e.$$set = (d) => {
    r(17, n = G(G({}, n), B(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, n = B(n), [o, l, u, f, c, i, s, t, R, S];
}
class Be extends Se {
  constructor(n) {
    super(), Le(this, n, qe, He, Te, {
      svelteInit: 5
    });
  }
}
const K = window.ms_globals.rerender, L = window.ms_globals.tree;
function Je(e) {
  function n(r) {
    const o = P(), l = new Be({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? L;
          return c.nodes = [...c.nodes, s], K({
            createPortal: M,
            node: L
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), K({
              createPortal: M,
              node: L
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
      r(n);
    });
  });
}
const Ye = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ke(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const o = e[r];
    return typeof o == "number" && !Ye.includes(r) ? n[r] = o + "px" : n[r] = o, n;
  }, {}) : {};
}
function V(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(M(I.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: I.Children.toArray(e._reactElement.props.children).map((l) => {
        if (I.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = V(l.props.el);
          return I.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...I.Children.toArray(l.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
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
    const t = o[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = V(t);
      n.push(...c), r.appendChild(s);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Qe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const b = he(({
  slot: e,
  clone: n,
  className: r,
  style: o
}, l) => {
  const t = ve(), [s, c] = ge([]);
  return we(() => {
    var f;
    if (!t.current || !e)
      return;
    let i = e;
    function p() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Qe(l, a), r && a.classList.add(...r.split(" ")), o) {
        const _ = Ke(o);
        Object.keys(_).forEach((m) => {
          a.style[m] = _[m];
        });
      }
    }
    let u = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var y, x, R;
        (y = t.current) != null && y.contains(i) && ((x = t.current) == null || x.removeChild(i));
        const {
          portals: m,
          clonedElement: v
        } = V(e);
        return i = v, c(m), i.style.display = "contents", p(), (R = t.current) == null || R.appendChild(i), m.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", p(), (f = t.current) == null || f.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((_ = t.current) == null || _.removeChild(i)), u == null || u.disconnect();
    };
  }, [e, n, r, o, l]), I.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Xe(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Ze(e, n = !1) {
  try {
    if (n && !Xe(e))
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
function k(e, n) {
  return g(() => Ze(e, n), [e, n]);
}
function re(e, n, r) {
  return e.filter(Boolean).map((o, l) => {
    var i;
    if (typeof o != "object")
      return o;
    const t = {
      ...o.props,
      key: ((i = o.props) == null ? void 0 : i.key) ?? (r ? `${r}-${l}` : `${l}`)
    };
    let s = t;
    Object.keys(o.slots).forEach((p) => {
      if (!o.slots[p] || !(o.slots[p] instanceof Element) && !o.slots[p].el)
        return;
      const u = p.split(".");
      u.forEach((v, y) => {
        s[v] || (s[v] = {}), y !== u.length - 1 && (s = t[v]);
      });
      const f = o.slots[p];
      let a, _, m = !1;
      f instanceof Element ? a = f : (a = f.el, _ = f.callback, m = f.clone ?? !1), s[u[u.length - 1]] = a ? _ ? (...v) => (_(u[u.length - 1], v), /* @__PURE__ */ h.jsx(b, {
        slot: a,
        clone: m
      })) : /* @__PURE__ */ h.jsx(b, {
        slot: a,
        clone: m
      }) : s[u[u.length - 1]], s = t;
    });
    const c = "children";
    return o[c] && (t[c] = re(o[c], n, `${l}`)), t;
  });
}
function $e(e, n) {
  return e ? /* @__PURE__ */ h.jsx(b, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function T({
  key: e,
  setSlotParams: n,
  slots: r
}, o) {
  return r[e] ? (...l) => (n(e, l), $e(r[e], {
    clone: !0,
    ...o
  })) : void 0;
}
function w(e) {
  return Array.isArray(e) ? e.map((n) => w(n)) : z(typeof e == "number" ? e * 1e3 : e);
}
function Q(e) {
  return Array.isArray(e) ? e.map((n) => n ? n.valueOf() / 1e3 : null) : typeof e == "object" && e !== null ? e.valueOf() / 1e3 : e;
}
const tt = Je(({
  slots: e,
  disabledDate: n,
  disabledTime: r,
  value: o,
  defaultValue: l,
  defaultPickerValue: t,
  pickerValue: s,
  showTime: c,
  presets: i,
  presetItems: p,
  onChange: u,
  minDate: f,
  maxDate: a,
  cellRender: _,
  panelRender: m,
  getPopupContainer: v,
  onValueChange: y,
  onPanelChange: x,
  children: R,
  setSlotParams: S,
  elRef: d,
  ...E
}) => {
  const oe = k(n), le = k(r), se = k(v), ce = k(_), ie = k(m), ae = g(() => typeof c == "object" ? {
    ...c,
    defaultValue: c.defaultValue ? w(c.defaultValue) : void 0
  } : c, [c]), ue = g(() => o ? w(o) : void 0, [o]), de = g(() => l ? w(l) : void 0, [l]), fe = g(() => t ? w(t) : void 0, [t]), pe = g(() => s ? w(s) : void 0, [s]), _e = g(() => f ? w(f) : void 0, [f]), me = g(() => a ? w(a) : void 0, [a]);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: R
    }), /* @__PURE__ */ h.jsx(ye, {
      ...E,
      ref: d,
      value: ue,
      defaultValue: de,
      defaultPickerValue: fe,
      pickerValue: pe,
      minDate: _e,
      maxDate: me,
      showTime: ae,
      disabledDate: oe,
      disabledTime: le,
      getPopupContainer: se,
      cellRender: e.cellRender ? T({
        slots: e,
        setSlotParams: S,
        key: "cellRender"
      }) : ce,
      panelRender: e.panelRender ? T({
        slots: e,
        setSlotParams: S,
        key: "panelRender"
      }) : ie,
      presets: g(() => (i || re(p)).map((C) => ({
        ...C,
        value: w(C.value)
      })), [i, p]),
      onPanelChange: (C, ...A) => {
        const O = Q(C);
        x == null || x(O, ...A);
      },
      onChange: (C, ...A) => {
        const O = Q(C);
        u == null || u(O, ...A), y(O);
      },
      renderExtraFooter: e.renderExtraFooter ? T({
        slots: e,
        setSlotParams: S,
        key: "renderExtraFooter"
      }) : E.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ h.jsx(b, {
        slot: e.prevIcon
      }) : E.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ h.jsx(b, {
        slot: e.nextIcon
      }) : E.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ h.jsx(b, {
        slot: e.suffixIcon
      }) : E.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ h.jsx(b, {
        slot: e.superNextIcon
      }) : E.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ h.jsx(b, {
        slot: e.superPrevIcon
      }) : E.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ h.jsx(b, {
          slot: e["allowClear.clearIcon"]
        })
      } : E.allowClear
    })]
  });
});
export {
  tt as DatePicker,
  tt as default
};
