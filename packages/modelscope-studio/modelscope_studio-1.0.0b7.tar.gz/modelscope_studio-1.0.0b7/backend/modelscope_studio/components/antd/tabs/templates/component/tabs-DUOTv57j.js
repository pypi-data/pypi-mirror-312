import { g as ee, w as C } from "./Index-Py8f6Hhx.js";
const w = window.ms_globals.React, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, M = window.ms_globals.React.useMemo, j = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Tabs;
var U = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = w, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(e, n, r) {
  var o, s = {}, t = null, l = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (o in n) se.call(n, o) && !ie.hasOwnProperty(o) && (s[o] = n[o]);
  if (e && e.defaultProps) for (o in n = e.defaultProps, n) s[o] === void 0 && (s[o] = n[o]);
  return {
    $$typeof: re,
    type: e,
    key: t,
    ref: l,
    props: s,
    _owner: le.current
  };
}
R.Fragment = oe;
R.jsx = G;
R.jsxs = G;
U.exports = R;
var h = U.exports;
const {
  SvelteComponent: ae,
  assign: B,
  binding_callbacks: L,
  check_outros: ce,
  children: H,
  claim_element: q,
  claim_space: ue,
  component_subscribe: F,
  compute_slots: de,
  create_slot: fe,
  detach: v,
  element: V,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: _e,
  get_slot_changes: pe,
  group_outros: he,
  init: me,
  insert_hydration: I,
  safe_not_equal: ge,
  set_custom_element_data: J,
  space: be,
  transition_in: S,
  transition_out: k,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ve,
  onDestroy: xe,
  setContext: ye
} = window.__gradio__svelte__internal;
function z(e) {
  let n, r;
  const o = (
    /*#slots*/
    e[7].default
  ), s = fe(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = V("svelte-slot"), s && s.c(), this.h();
    },
    l(t) {
      n = q(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = H(n);
      s && s.l(l), l.forEach(v), this.h();
    },
    h() {
      J(n, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      I(t, n, l), s && s.m(n, null), e[9](n), r = !0;
    },
    p(t, l) {
      s && s.p && (!r || l & /*$$scope*/
      64) && we(
        s,
        o,
        t,
        /*$$scope*/
        t[6],
        r ? pe(
          o,
          /*$$scope*/
          t[6],
          l,
          null
        ) : _e(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (S(s, t), r = !0);
    },
    o(t) {
      k(s, t), r = !1;
    },
    d(t) {
      t && v(n), s && s.d(t), e[9](null);
    }
  };
}
function Ce(e) {
  let n, r, o, s, t = (
    /*$$slots*/
    e[4].default && z(e)
  );
  return {
    c() {
      n = V("react-portal-target"), r = be(), t && t.c(), o = N(), this.h();
    },
    l(l) {
      n = q(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(n).forEach(v), r = ue(l), t && t.l(l), o = N(), this.h();
    },
    h() {
      J(n, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      I(l, n, a), e[8](n), I(l, r, a), t && t.m(l, a), I(l, o, a), s = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, a), a & /*$$slots*/
      16 && S(t, 1)) : (t = z(l), t.c(), S(t, 1), t.m(o.parentNode, o)) : t && (he(), k(t, 1, 1, () => {
        t = null;
      }), ce());
    },
    i(l) {
      s || (S(t), s = !0);
    },
    o(l) {
      k(t), s = !1;
    },
    d(l) {
      l && (v(n), v(r), v(o)), e[8](null), t && t.d(l);
    }
  };
}
function W(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function Ie(e, n, r) {
  let o, s, {
    $$slots: t = {},
    $$scope: l
  } = n;
  const a = de(t);
  let {
    svelteInit: i
  } = n;
  const f = C(W(n)), c = C();
  F(e, c, (d) => r(0, o = d));
  const _ = C();
  F(e, _, (d) => r(1, s = d));
  const u = [], p = ve("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: g,
    subSlotIndex: E
  } = ee() || {}, x = i({
    parent: p,
    props: f,
    target: c,
    slot: _,
    slotKey: m,
    slotIndex: g,
    subSlotIndex: E,
    onDestroy(d) {
      u.push(d);
    }
  });
  ye("$$ms-gr-react-wrapper", x), Ee(() => {
    f.set(W(n));
  }), xe(() => {
    u.forEach((d) => d());
  });
  function y(d) {
    L[d ? "unshift" : "push"](() => {
      o = d, c.set(o);
    });
  }
  function K(d) {
    L[d ? "unshift" : "push"](() => {
      s = d, _.set(s);
    });
  }
  return e.$$set = (d) => {
    r(17, n = B(B({}, n), A(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, l = d.$$scope);
  }, n = A(n), [o, s, c, _, a, i, l, t, y, K];
}
class Se extends ae {
  constructor(n) {
    super(), me(this, n, Ie, Ce, ge, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, P = window.ms_globals.tree;
function Re(e) {
  function n(r) {
    const o = C(), s = new Se({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
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
          }, a = t.parent ?? P;
          return a.nodes = [...a.nodes, l], D({
            createPortal: j,
            node: P
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== o), D({
              createPortal: j,
              node: P
            });
          }), l;
        },
        ...r.props
      }
    });
    return o.set(s), s;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const o = e[r];
    return typeof o == "number" && !Pe.includes(r) ? n[r] = o + "px" : n[r] = o, n;
  }, {}) : {};
}
function T(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(j(w.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: w.Children.toArray(e._reactElement.props.children).map((s) => {
        if (w.isValidElement(s) && s.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = T(s.props.el);
          return w.cloneElement(s, {
            ...s.props,
            el: l,
            children: [...w.Children.toArray(s.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((s) => {
    e.getEventListeners(s).forEach(({
      listener: l,
      type: a,
      useCapture: i
    }) => {
      r.addEventListener(a, l, i);
    });
  });
  const o = Array.from(e.childNodes);
  for (let s = 0; s < o.length; s++) {
    const t = o[s];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = T(t);
      n.push(...a), r.appendChild(l);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function je(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const b = Q(({
  slot: e,
  clone: n,
  className: r,
  style: o
}, s) => {
  const t = X(), [l, a] = Z([]);
  return $(() => {
    var _;
    if (!t.current || !e)
      return;
    let i = e;
    function f() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), je(s, u), r && u.classList.add(...r.split(" ")), o) {
        const p = Oe(o);
        Object.keys(p).forEach((m) => {
          u.style[m] = p[m];
        });
      }
    }
    let c = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var E, x, y;
        (E = t.current) != null && E.contains(i) && ((x = t.current) == null || x.removeChild(i));
        const {
          portals: m,
          clonedElement: g
        } = T(e);
        return i = g, a(m), i.style.display = "contents", f(), (y = t.current) == null || y.appendChild(i), m.length > 0;
      };
      u() || (c = new window.MutationObserver(() => {
        u() && (c == null || c.disconnect());
      }), c.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", f(), (_ = t.current) == null || _.appendChild(i);
    return () => {
      var u, p;
      i.style.display = "", (u = t.current) != null && u.contains(i) && ((p = t.current) == null || p.removeChild(i)), c == null || c.disconnect();
    };
  }, [e, n, r, o, s]), w.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function ke(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Te(e, n = !1) {
  try {
    if (n && !ke(e))
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
function O(e, n) {
  return M(() => Te(e, n), [e, n]);
}
function Be(e) {
  return Object.keys(e).reduce((n, r) => (e[r] !== void 0 && (n[r] = e[r]), n), {});
}
function Y(e, n, r) {
  return e.filter(Boolean).map((o, s) => {
    var i;
    if (typeof o != "object")
      return o;
    const t = {
      ...o.props,
      key: ((i = o.props) == null ? void 0 : i.key) ?? (r ? `${r}-${s}` : `${s}`)
    };
    let l = t;
    Object.keys(o.slots).forEach((f) => {
      if (!o.slots[f] || !(o.slots[f] instanceof Element) && !o.slots[f].el)
        return;
      const c = f.split(".");
      c.forEach((g, E) => {
        l[g] || (l[g] = {}), E !== c.length - 1 && (l = t[g]);
      });
      const _ = o.slots[f];
      let u, p, m = !1;
      _ instanceof Element ? u = _ : (u = _.el, p = _.callback, m = _.clone ?? !1), l[c[c.length - 1]] = u ? p ? (...g) => (p(c[c.length - 1], g), /* @__PURE__ */ h.jsx(b, {
        slot: u,
        clone: m
      })) : /* @__PURE__ */ h.jsx(b, {
        slot: u,
        clone: m
      }) : l[c[c.length - 1]], l = t;
    });
    const a = "children";
    return o[a] && (t[a] = Y(o[a], n, `${s}`)), t;
  });
}
function Le(e, n) {
  return e ? /* @__PURE__ */ h.jsx(b, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Fe({
  key: e,
  setSlotParams: n,
  slots: r
}, o) {
  return r[e] ? (...s) => (n(e, s), Le(r[e], {
    clone: !0,
    ...o
  })) : void 0;
}
const Ae = Re(({
  slots: e,
  indicator: n,
  items: r,
  onChange: o,
  slotItems: s,
  more: t,
  children: l,
  renderTabBar: a,
  setSlotParams: i,
  ...f
}) => {
  const c = O(n == null ? void 0 : n.size), _ = O(t == null ? void 0 : t.getPopupContainer), u = O(a);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: l
    }), /* @__PURE__ */ h.jsx(te, {
      ...f,
      indicator: c ? {
        ...n,
        size: c
      } : n,
      renderTabBar: e.renderTabBar ? Fe({
        slots: e,
        setSlotParams: i,
        key: "renderTabBar"
      }) : u,
      items: M(() => r || Y(s), [r, s]),
      more: Be({
        ...t || {},
        getPopupContainer: _ || (t == null ? void 0 : t.getPopupContainer),
        icon: e["more.icon"] ? /* @__PURE__ */ h.jsx(b, {
          slot: e["more.icon"]
        }) : t == null ? void 0 : t.icon
      }),
      tabBarExtraContent: e.tabBarExtraContent ? /* @__PURE__ */ h.jsx(b, {
        slot: e.tabBarExtraContent
      }) : e["tabBarExtraContent.left"] || e["tabBarExtraContent.right"] ? {
        left: e["tabBarExtraContent.left"] ? /* @__PURE__ */ h.jsx(b, {
          slot: e["tabBarExtraContent.left"]
        }) : void 0,
        right: e["tabBarExtraContent.right"] ? /* @__PURE__ */ h.jsx(b, {
          slot: e["tabBarExtraContent.right"]
        }) : void 0
      } : f.tabBarExtraContent,
      addIcon: e.addIcon ? /* @__PURE__ */ h.jsx(b, {
        slot: e.addIcon
      }) : f.addIcon,
      removeIcon: e.removeIcon ? /* @__PURE__ */ h.jsx(b, {
        slot: e.removeIcon
      }) : f.removeIcon,
      onChange: (p) => {
        o == null || o(p);
      }
    })]
  });
});
export {
  Ae as Tabs,
  Ae as default
};
