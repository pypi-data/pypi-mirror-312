import { g as ve, w as F } from "./Index-BOuIu9y-.js";
const j = window.ms_globals.React, me = window.ms_globals.React.forwardRef, he = window.ms_globals.React.useRef, we = window.ms_globals.React.useState, ge = window.ms_globals.React.useEffect, E = window.ms_globals.React.useMemo, W = window.ms_globals.ReactDOM.createPortal, ye = window.ms_globals.antd.DatePicker, U = window.ms_globals.dayjs;
var Z = {
  exports: {}
}, L = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var be = j, xe = Symbol.for("react.element"), Ee = Symbol.for("react.fragment"), Ie = Object.prototype.hasOwnProperty, Re = be.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, je = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, n, r) {
  var o, l = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (o in n) Ie.call(n, o) && !je.hasOwnProperty(o) && (l[o] = n[o]);
  if (e && e.defaultProps) for (o in n = e.defaultProps, n) l[o] === void 0 && (l[o] = n[o]);
  return {
    $$typeof: xe,
    type: e,
    key: t,
    ref: s,
    props: l,
    _owner: Re.current
  };
}
L.Fragment = Ee;
L.jsx = V;
L.jsxs = V;
Z.exports = L;
var w = Z.exports;
const {
  SvelteComponent: Se,
  assign: H,
  binding_callbacks: q,
  check_outros: Oe,
  children: $,
  claim_element: ee,
  claim_space: Pe,
  component_subscribe: B,
  compute_slots: ke,
  create_slot: Ce,
  detach: P,
  element: te,
  empty: J,
  exclude_internal_props: Y,
  get_all_dirty_from_scope: De,
  get_slot_changes: Fe,
  group_outros: Ne,
  init: Ae,
  insert_hydration: N,
  safe_not_equal: Le,
  set_custom_element_data: ne,
  space: Te,
  transition_in: A,
  transition_out: z,
  update_slot_base: Me
} = window.__gradio__svelte__internal, {
  beforeUpdate: We,
  getContext: ze,
  onDestroy: Ge,
  setContext: Ue
} = window.__gradio__svelte__internal;
function K(e) {
  let n, r;
  const o = (
    /*#slots*/
    e[7].default
  ), l = Ce(
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
      l && l.l(s), s.forEach(P), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      N(t, n, s), l && l.m(n, null), e[9](n), r = !0;
    },
    p(t, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && Me(
        l,
        o,
        t,
        /*$$scope*/
        t[6],
        r ? Fe(
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
      r || (A(l, t), r = !0);
    },
    o(t) {
      z(l, t), r = !1;
    },
    d(t) {
      t && P(n), l && l.d(t), e[9](null);
    }
  };
}
function He(e) {
  let n, r, o, l, t = (
    /*$$slots*/
    e[4].default && K(e)
  );
  return {
    c() {
      n = te("react-portal-target"), r = Te(), t && t.c(), o = J(), this.h();
    },
    l(s) {
      n = ee(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), $(n).forEach(P), r = Pe(s), t && t.l(s), o = J(), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      N(s, n, i), e[8](n), N(s, r, i), t && t.m(s, i), N(s, o, i), l = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, i), i & /*$$slots*/
      16 && A(t, 1)) : (t = K(s), t.c(), A(t, 1), t.m(o.parentNode, o)) : t && (Ne(), z(t, 1, 1, () => {
        t = null;
      }), Oe());
    },
    i(s) {
      l || (A(t), l = !0);
    },
    o(s) {
      z(t), l = !1;
    },
    d(s) {
      s && (P(n), P(r), P(o)), e[8](null), t && t.d(s);
    }
  };
}
function Q(e) {
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
  const i = ke(t);
  let {
    svelteInit: c
  } = n;
  const _ = F(Q(n)), a = F();
  B(e, a, (d) => r(0, o = d));
  const p = F();
  B(e, p, (d) => r(1, l = d));
  const u = [], m = ze("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: g,
    subSlotIndex: v
  } = ve() || {}, I = c({
    parent: m,
    props: _,
    target: a,
    slot: p,
    slotKey: h,
    slotIndex: g,
    subSlotIndex: v,
    onDestroy(d) {
      u.push(d);
    }
  });
  Ue("$$ms-gr-react-wrapper", I), We(() => {
    _.set(Q(n));
  }), Ge(() => {
    u.forEach((d) => d());
  });
  function S(d) {
    q[d ? "unshift" : "push"](() => {
      o = d, a.set(o);
    });
  }
  function k(d) {
    q[d ? "unshift" : "push"](() => {
      l = d, p.set(l);
    });
  }
  return e.$$set = (d) => {
    r(17, n = H(H({}, n), Y(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, n = Y(n), [o, l, a, p, i, c, s, t, S, k];
}
class Be extends Se {
  constructor(n) {
    super(), Ae(this, n, qe, He, Le, {
      svelteInit: 5
    });
  }
}
const X = window.ms_globals.rerender, T = window.ms_globals.tree;
function Je(e) {
  function n(r) {
    const o = F(), l = new Be({
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
          }, i = t.parent ?? T;
          return i.nodes = [...i.nodes, s], X({
            createPortal: W,
            node: T
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== o), X({
              createPortal: W,
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
function G(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(W(j.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: j.Children.toArray(e._reactElement.props.children).map((l) => {
        if (j.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = G(l.props.el);
          return j.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...j.Children.toArray(l.props.children), ...t]
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
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, s, c);
    });
  });
  const o = Array.from(e.childNodes);
  for (let l = 0; l < o.length; l++) {
    const t = o[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = G(t);
      n.push(...i), r.appendChild(s);
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
const y = me(({
  slot: e,
  clone: n,
  className: r,
  style: o
}, l) => {
  const t = he(), [s, i] = we([]);
  return ge(() => {
    var p;
    if (!t.current || !e)
      return;
    let c = e;
    function _() {
      let u = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (u = c.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Qe(l, u), r && u.classList.add(...r.split(" ")), o) {
        const m = Ke(o);
        Object.keys(m).forEach((h) => {
          u.style[h] = m[h];
        });
      }
    }
    let a = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var v, I, S;
        (v = t.current) != null && v.contains(c) && ((I = t.current) == null || I.removeChild(c));
        const {
          portals: h,
          clonedElement: g
        } = G(e);
        return c = g, i(h), c.style.display = "contents", _(), (S = t.current) == null || S.appendChild(c), h.length > 0;
      };
      u() || (a = new window.MutationObserver(() => {
        u() && (a == null || a.disconnect());
      }), a.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", _(), (p = t.current) == null || p.appendChild(c);
    return () => {
      var u, m;
      c.style.display = "", (u = t.current) != null && u.contains(c) && ((m = t.current) == null || m.removeChild(c)), a == null || a.disconnect();
    };
  }, [e, n, r, o, l]), j.createElement("react-child", {
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
function C(e, n) {
  return E(() => Ze(e, n), [e, n]);
}
function re(e, n, r) {
  return e.filter(Boolean).map((o, l) => {
    var c;
    if (typeof o != "object")
      return o;
    const t = {
      ...o.props,
      key: ((c = o.props) == null ? void 0 : c.key) ?? (r ? `${r}-${l}` : `${l}`)
    };
    let s = t;
    Object.keys(o.slots).forEach((_) => {
      if (!o.slots[_] || !(o.slots[_] instanceof Element) && !o.slots[_].el)
        return;
      const a = _.split(".");
      a.forEach((g, v) => {
        s[g] || (s[g] = {}), v !== a.length - 1 && (s = t[g]);
      });
      const p = o.slots[_];
      let u, m, h = !1;
      p instanceof Element ? u = p : (u = p.el, m = p.callback, h = p.clone ?? !1), s[a[a.length - 1]] = u ? m ? (...g) => (m(a[a.length - 1], g), /* @__PURE__ */ w.jsx(y, {
        slot: u,
        clone: h
      })) : /* @__PURE__ */ w.jsx(y, {
        slot: u,
        clone: h
      }) : s[a[a.length - 1]], s = t;
    });
    const i = "children";
    return o[i] && (t[i] = re(o[i], n, `${l}`)), t;
  });
}
function Ve(e, n) {
  return e ? /* @__PURE__ */ w.jsx(y, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function M({
  key: e,
  setSlotParams: n,
  slots: r
}, o) {
  return r[e] ? (...l) => (n(e, l), Ve(r[e], {
    clone: !0,
    ...o
  })) : void 0;
}
function x(e) {
  return U(typeof e == "number" ? e * 1e3 : e);
}
function D(e) {
  return (e == null ? void 0 : e.map((n) => n ? n.valueOf() / 1e3 : null)) || [null, null];
}
const et = Je(({
  slots: e,
  disabledDate: n,
  value: r,
  defaultValue: o,
  defaultPickerValue: l,
  pickerValue: t,
  presets: s,
  presetItems: i,
  showTime: c,
  onChange: _,
  minDate: a,
  maxDate: p,
  cellRender: u,
  panelRender: m,
  getPopupContainer: h,
  onValueChange: g,
  onPanelChange: v,
  onCalendarChange: I,
  children: S,
  setSlotParams: k,
  elRef: d,
  ...b
}) => {
  const oe = C(n), le = C(h), se = C(u), ce = C(m), ie = E(() => {
    var f;
    return typeof c == "object" ? {
      ...c,
      defaultValue: (f = c.defaultValue) == null ? void 0 : f.map((R) => x(R))
    } : c;
  }, [c]), ae = E(() => r == null ? void 0 : r.map((f) => x(f)), [r]), ue = E(() => o == null ? void 0 : o.map((f) => x(f)), [o]), de = E(() => Array.isArray(l) ? l.map((f) => x(f)) : l ? x(l) : void 0, [l]), fe = E(() => Array.isArray(t) ? t.map((f) => x(f)) : t ? x(t) : void 0, [t]), pe = E(() => a ? x(a) : void 0, [a]), _e = E(() => p ? x(p) : void 0, [p]);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: S
    }), /* @__PURE__ */ w.jsx(ye.RangePicker, {
      ...b,
      ref: d,
      value: ae,
      defaultValue: ue,
      defaultPickerValue: de,
      pickerValue: fe,
      minDate: pe,
      maxDate: _e,
      showTime: ie,
      disabledDate: oe,
      getPopupContainer: le,
      cellRender: e.cellRender ? M({
        slots: e,
        setSlotParams: k,
        key: "cellRender"
      }) : se,
      panelRender: e.panelRender ? M({
        slots: e,
        setSlotParams: k,
        key: "panelRender"
      }) : ce,
      presets: E(() => (s || re(i)).map((f) => ({
        ...f,
        value: D(f.value)
      })), [s, i]),
      onPanelChange: (f, ...R) => {
        const O = D(f);
        v == null || v(O, ...R);
      },
      onChange: (f, ...R) => {
        const O = D(f);
        _ == null || _(O, ...R), g(O);
      },
      onCalendarChange: (f, ...R) => {
        const O = D(f);
        I == null || I(O, ...R);
      },
      renderExtraFooter: e.renderExtraFooter ? M({
        slots: e,
        setSlotParams: k,
        key: "renderExtraFooter"
      }) : b.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ w.jsx(y, {
        slot: e.prevIcon
      }) : b.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ w.jsx(y, {
        slot: e.nextIcon
      }) : b.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ w.jsx(y, {
        slot: e.suffixIcon
      }) : b.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ w.jsx(y, {
        slot: e.superNextIcon
      }) : b.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ w.jsx(y, {
        slot: e.superPrevIcon
      }) : b.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ w.jsx(y, {
          slot: e["allowClear.clearIcon"]
        })
      } : b.allowClear,
      separator: e.separator ? /* @__PURE__ */ w.jsx(y, {
        slot: e.separator,
        clone: !0
      }) : b.separator
    })]
  });
});
export {
  et as DateRangePicker,
  et as default
};
