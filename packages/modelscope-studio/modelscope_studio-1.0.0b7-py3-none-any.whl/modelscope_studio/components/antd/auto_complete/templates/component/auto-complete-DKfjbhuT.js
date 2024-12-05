import { b as ee, g as te, w as x } from "./Index-D5EPKil0.js";
const y = window.ms_globals.React, U = window.ms_globals.React.forwardRef, P = window.ms_globals.React.useRef, H = window.ms_globals.React.useState, j = window.ms_globals.React.useEffect, T = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.internalContext.AutoCompleteContext, re = window.ms_globals.antd.AutoComplete;
function le(t, e) {
  return ee(t, e);
}
var B = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var oe = y, se = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ie = Object.prototype.hasOwnProperty, ae = oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function J(t, e, r) {
  var l, o = {}, n = null, s = null;
  r !== void 0 && (n = "" + r), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (l in e) ie.call(e, l) && !ue.hasOwnProperty(l) && (o[l] = e[l]);
  if (t && t.defaultProps) for (l in e = t.defaultProps, e) o[l] === void 0 && (o[l] = e[l]);
  return {
    $$typeof: se,
    type: t,
    key: n,
    ref: s,
    props: o,
    _owner: ae.current
  };
}
I.Fragment = ce;
I.jsx = J;
I.jsxs = J;
B.exports = I;
var m = B.exports;
const {
  SvelteComponent: de,
  assign: N,
  binding_callbacks: W,
  check_outros: fe,
  children: Y,
  claim_element: K,
  claim_space: _e,
  component_subscribe: V,
  compute_slots: pe,
  create_slot: he,
  detach: E,
  element: Q,
  empty: D,
  exclude_internal_props: M,
  get_all_dirty_from_scope: me,
  get_slot_changes: ge,
  group_outros: we,
  init: be,
  insert_hydration: R,
  safe_not_equal: ye,
  set_custom_element_data: X,
  space: Ce,
  transition_in: S,
  transition_out: A,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: xe,
  onDestroy: Re,
  setContext: Se
} = window.__gradio__svelte__internal;
function q(t) {
  let e, r;
  const l = (
    /*#slots*/
    t[7].default
  ), o = he(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = Q("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      e = K(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(e);
      o && o.l(s), s.forEach(E), this.h();
    },
    h() {
      X(e, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      R(n, e, s), o && o.m(e, null), t[9](e), r = !0;
    },
    p(n, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && Ee(
        o,
        l,
        n,
        /*$$scope*/
        n[6],
        r ? ge(
          l,
          /*$$scope*/
          n[6],
          s,
          null
        ) : me(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (S(o, n), r = !0);
    },
    o(n) {
      A(o, n), r = !1;
    },
    d(n) {
      n && E(e), o && o.d(n), t[9](null);
    }
  };
}
function Ie(t) {
  let e, r, l, o, n = (
    /*$$slots*/
    t[4].default && q(t)
  );
  return {
    c() {
      e = Q("react-portal-target"), r = Ce(), n && n.c(), l = D(), this.h();
    },
    l(s) {
      e = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(e).forEach(E), r = _e(s), n && n.l(s), l = D(), this.h();
    },
    h() {
      X(e, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      R(s, e, i), t[8](e), R(s, r, i), n && n.m(s, i), R(s, l, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, i), i & /*$$slots*/
      16 && S(n, 1)) : (n = q(s), n.c(), S(n, 1), n.m(l.parentNode, l)) : n && (we(), A(n, 1, 1, () => {
        n = null;
      }), fe());
    },
    i(s) {
      o || (S(n), o = !0);
    },
    o(s) {
      A(n), o = !1;
    },
    d(s) {
      s && (E(e), E(r), E(l)), t[8](null), n && n.d(s);
    }
  };
}
function z(t) {
  const {
    svelteInit: e,
    ...r
  } = t;
  return r;
}
function Oe(t, e, r) {
  let l, o, {
    $$slots: n = {},
    $$scope: s
  } = e;
  const i = pe(n);
  let {
    svelteInit: c
  } = e;
  const h = x(z(e)), u = x();
  V(t, u, (d) => r(0, l = d));
  const f = x();
  V(t, f, (d) => r(1, o = d));
  const a = [], _ = xe("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: g,
    subSlotIndex: w
  } = te() || {}, b = c({
    parent: _,
    props: h,
    target: u,
    slot: f,
    slotKey: p,
    slotIndex: g,
    subSlotIndex: w,
    onDestroy(d) {
      a.push(d);
    }
  });
  Se("$$ms-gr-react-wrapper", b), ve(() => {
    h.set(z(e));
  }), Re(() => {
    a.forEach((d) => d());
  });
  function C(d) {
    W[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function $(d) {
    W[d ? "unshift" : "push"](() => {
      o = d, f.set(o);
    });
  }
  return t.$$set = (d) => {
    r(17, e = N(N({}, e), M(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, e = M(e), [l, o, u, f, i, c, s, n, C, $];
}
class ke extends de {
  constructor(e) {
    super(), be(this, e, Oe, Ie, ye, {
      svelteInit: 5
    });
  }
}
const G = window.ms_globals.rerender, O = window.ms_globals.tree;
function Pe(t) {
  function e(r) {
    const l = x(), o = new ke({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: t,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, i = n.parent ?? O;
          return i.nodes = [...i.nodes, s], G({
            createPortal: F,
            node: O
          }), n.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), G({
              createPortal: F,
              node: O
            });
          }), s;
        },
        ...r.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(e);
    });
  });
}
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Fe(t) {
  return t ? Object.keys(t).reduce((e, r) => {
    const l = t[r];
    return typeof l == "number" && !je.includes(r) ? e[r] = l + "px" : e[r] = l, e;
  }, {}) : {};
}
function L(t) {
  const e = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return e.push(F(y.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: y.Children.toArray(t._reactElement.props.children).map((o) => {
        if (y.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = L(o.props.el);
          return y.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...y.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: s,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, s, c);
    });
  });
  const l = Array.from(t.childNodes);
  for (let o = 0; o < l.length; o++) {
    const n = l[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = L(n);
      e.push(...i), r.appendChild(s);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Ae(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const v = U(({
  slot: t,
  clone: e,
  className: r,
  style: l
}, o) => {
  const n = P(), [s, i] = H([]);
  return j(() => {
    var f;
    if (!n.current || !t)
      return;
    let c = t;
    function h() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ae(o, a), r && a.classList.add(...r.split(" ")), l) {
        const _ = Fe(l);
        Object.keys(_).forEach((p) => {
          a.style[p] = _[p];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var w, b, C;
        (w = n.current) != null && w.contains(c) && ((b = n.current) == null || b.removeChild(c));
        const {
          portals: p,
          clonedElement: g
        } = L(t);
        return c = g, i(p), c.style.display = "contents", h(), (C = n.current) == null || C.appendChild(c), p.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", h(), (f = n.current) == null || f.appendChild(c);
    return () => {
      var a, _;
      c.style.display = "", (a = n.current) != null && a.contains(c) && ((_ = n.current) == null || _.removeChild(c)), u == null || u.disconnect();
    };
  }, [t, e, r, l, o]), y.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function Te(t, e = !1) {
  try {
    if (e && !Le(t))
      return;
    if (typeof t == "string") {
      let r = t.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function k(t, e) {
  return T(() => Te(t, e), [t, e]);
}
function Ne({
  value: t,
  onValueChange: e
}) {
  const [r, l] = H(t), o = P(e);
  o.current = e;
  const n = P(r);
  return n.current = r, j(() => {
    o.current(r);
  }, [r]), j(() => {
    le(t, n.current) || l(t);
  }, [t]), [r, l];
}
function Z(t, e, r) {
  return t.filter(Boolean).map((l, o) => {
    var c;
    if (typeof l != "object")
      return e != null && e.fallback ? e.fallback(l) : l;
    const n = {
      ...l.props,
      key: ((c = l.props) == null ? void 0 : c.key) ?? (r ? `${r}-${o}` : `${o}`)
    };
    let s = n;
    Object.keys(l.slots).forEach((h) => {
      if (!l.slots[h] || !(l.slots[h] instanceof Element) && !l.slots[h].el)
        return;
      const u = h.split(".");
      u.forEach((g, w) => {
        s[g] || (s[g] = {}), w !== u.length - 1 && (s = n[g]);
      });
      const f = l.slots[h];
      let a, _, p = (e == null ? void 0 : e.clone) ?? !1;
      f instanceof Element ? a = f : (a = f.el, _ = f.callback, p = f.clone ?? !1), s[u[u.length - 1]] = a ? _ ? (...g) => (_(u[u.length - 1], g), /* @__PURE__ */ m.jsx(v, {
        slot: a,
        clone: p
      })) : /* @__PURE__ */ m.jsx(v, {
        slot: a,
        clone: p
      }) : s[u[u.length - 1]], s = n;
    });
    const i = (e == null ? void 0 : e.children) || "children";
    return l[i] && (n[i] = Z(l[i], e, `${o}`)), n;
  });
}
function We(t, e) {
  return t ? /* @__PURE__ */ m.jsx(v, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Ve({
  key: t,
  setSlotParams: e,
  slots: r
}, l) {
  return r[t] ? (...o) => (e(t, o), We(r[t], {
    clone: !0,
    ...l
  })) : void 0;
}
const De = U(({
  children: t,
  ...e
}, r) => /* @__PURE__ */ m.jsx(ne.Provider, {
  value: T(() => ({
    ...e,
    elRef: r
  }), [e, r]),
  children: t
})), qe = Pe(({
  slots: t,
  children: e,
  onValueChange: r,
  filterOption: l,
  onChange: o,
  options: n,
  optionItems: s,
  getPopupContainer: i,
  dropdownRender: c,
  elRef: h,
  setSlotParams: u,
  ...f
}) => {
  const a = k(i), _ = k(l), p = k(c), [g, w] = Ne({
    onValueChange: r,
    value: f.value
  });
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [t.children ? null : /* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ m.jsx(re, {
      ...f,
      value: g,
      ref: h,
      allowClear: t["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(v, {
          slot: t["allowClear.clearIcon"]
        })
      } : f.allowClear,
      options: T(() => n || Z(s, {
        children: "options",
        clone: !0
      }), [s, n]),
      onChange: (b, ...C) => {
        o == null || o(b, ...C), w(b);
      },
      notFoundContent: t.notFoundContent ? /* @__PURE__ */ m.jsx(v, {
        slot: t.notFoundContent
      }) : f.notFoundContent,
      filterOption: _ || l,
      getPopupContainer: a,
      dropdownRender: t.dropdownRender ? Ve({
        slots: t,
        setSlotParams: u,
        key: "dropdownRender"
      }, {
        clone: !0
      }) : p,
      children: t.children ? /* @__PURE__ */ m.jsxs(De, {
        children: [/* @__PURE__ */ m.jsx("div", {
          style: {
            display: "none"
          },
          children: e
        }), /* @__PURE__ */ m.jsx(v, {
          slot: t.children
        })]
      }) : null
    })]
  });
});
export {
  qe as AutoComplete,
  qe as default
};
