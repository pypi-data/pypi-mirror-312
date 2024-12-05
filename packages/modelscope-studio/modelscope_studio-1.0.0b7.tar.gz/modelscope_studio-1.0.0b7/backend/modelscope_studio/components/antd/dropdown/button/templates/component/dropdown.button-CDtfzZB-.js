import { g as ne, w as R, d as re, a as v } from "./Index-BGUgCZQM.js";
const w = window.ms_globals.React, k = window.ms_globals.React.useMemo, H = window.ms_globals.React.useState, V = window.ms_globals.React.useEffect, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, L = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.Dropdown;
var q = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var se = w, le = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ie = Object.prototype.hasOwnProperty, ue = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function J(n, e, r) {
  var o, l = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) ie.call(e, o) && !ae.hasOwnProperty(o) && (l[o] = e[o]);
  if (n && n.defaultProps) for (o in e = n.defaultProps, e) l[o] === void 0 && (l[o] = e[o]);
  return {
    $$typeof: le,
    type: n,
    key: t,
    ref: s,
    props: l,
    _owner: ue.current
  };
}
O.Fragment = ce;
O.jsx = J;
O.jsxs = J;
q.exports = O;
var E = q.exports;
const {
  SvelteComponent: de,
  assign: F,
  binding_callbacks: N,
  check_outros: fe,
  children: Y,
  claim_element: K,
  claim_space: pe,
  component_subscribe: D,
  compute_slots: _e,
  create_slot: me,
  detach: y,
  element: Q,
  empty: W,
  exclude_internal_props: B,
  get_all_dirty_from_scope: he,
  get_slot_changes: ge,
  group_outros: we,
  init: be,
  insert_hydration: S,
  safe_not_equal: ye,
  set_custom_element_data: X,
  space: Ee,
  transition_in: C,
  transition_out: T,
  update_slot_base: ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: Ie,
  onDestroy: Re,
  setContext: Se
} = window.__gradio__svelte__internal;
function M(n) {
  let e, r;
  const o = (
    /*#slots*/
    n[7].default
  ), l = me(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = Q("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      e = K(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(e);
      l && l.l(s), s.forEach(y), this.h();
    },
    h() {
      X(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      S(t, e, s), l && l.m(e, null), n[9](e), r = !0;
    },
    p(t, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && ve(
        l,
        o,
        t,
        /*$$scope*/
        t[6],
        r ? ge(
          o,
          /*$$scope*/
          t[6],
          s,
          null
        ) : he(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (C(l, t), r = !0);
    },
    o(t) {
      T(l, t), r = !1;
    },
    d(t) {
      t && y(e), l && l.d(t), n[9](null);
    }
  };
}
function Ce(n) {
  let e, r, o, l, t = (
    /*$$slots*/
    n[4].default && M(n)
  );
  return {
    c() {
      e = Q("react-portal-target"), r = Ee(), t && t.c(), o = W(), this.h();
    },
    l(s) {
      e = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(e).forEach(y), r = pe(s), t && t.l(s), o = W(), this.h();
    },
    h() {
      X(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      S(s, e, c), n[8](e), S(s, r, c), t && t.m(s, c), S(s, o, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && C(t, 1)) : (t = M(s), t.c(), C(t, 1), t.m(o.parentNode, o)) : t && (we(), T(t, 1, 1, () => {
        t = null;
      }), fe());
    },
    i(s) {
      l || (C(t), l = !0);
    },
    o(s) {
      T(t), l = !1;
    },
    d(s) {
      s && (y(e), y(r), y(o)), n[8](null), t && t.d(s);
    }
  };
}
function z(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function ke(n, e, r) {
  let o, l, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const c = _e(t);
  let {
    svelteInit: i
  } = e;
  const h = R(z(e)), a = R();
  D(n, a, (d) => r(0, o = d));
  const f = R();
  D(n, f, (d) => r(1, l = d));
  const u = [], p = Ie("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: m,
    subSlotIndex: g
  } = ne() || {}, b = i({
    parent: p,
    props: h,
    target: a,
    slot: f,
    slotKey: _,
    slotIndex: m,
    subSlotIndex: g,
    onDestroy(d) {
      u.push(d);
    }
  });
  Se("$$ms-gr-react-wrapper", b), xe(() => {
    h.set(z(e));
  }), Re(() => {
    u.forEach((d) => d());
  });
  function I(d) {
    N[d ? "unshift" : "push"](() => {
      o = d, a.set(o);
    });
  }
  function $(d) {
    N[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  return n.$$set = (d) => {
    r(17, e = F(F({}, e), B(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, e = B(e), [o, l, a, f, c, i, s, t, I, $];
}
class Oe extends de {
  constructor(e) {
    super(), be(this, e, ke, Ce, ye, {
      svelteInit: 5
    });
  }
}
const G = window.ms_globals.rerender, P = window.ms_globals.tree;
function Pe(n) {
  function e(r) {
    const o = R(), l = new Oe({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
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
          }, c = t.parent ?? P;
          return c.nodes = [...c.nodes, s], G({
            createPortal: L,
            node: P
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), G({
              createPortal: L,
              node: P
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
      r(e);
    });
  });
}
function je(n) {
  const [e, r] = H(() => v(n));
  return V(() => {
    let o = !0;
    return n.subscribe((t) => {
      o && (o = !1, t === e) || r(t);
    });
  }, [n]), e;
}
function Le(n) {
  const e = k(() => re(n, (r) => r), [n]);
  return je(e);
}
const Te = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const o = n[r];
    return typeof o == "number" && !Te.includes(r) ? e[r] = o + "px" : e[r] = o, e;
  }, {}) : {};
}
function A(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(L(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((l) => {
        if (w.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = A(l.props.el);
          return w.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...w.Children.toArray(l.props.children), ...t]
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
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const o = Array.from(n.childNodes);
  for (let l = 0; l < o.length; l++) {
    const t = o[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = A(t);
      e.push(...c), r.appendChild(s);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Fe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const x = ee(({
  slot: n,
  clone: e,
  className: r,
  style: o
}, l) => {
  const t = te(), [s, c] = H([]);
  return V(() => {
    var f;
    if (!t.current || !n)
      return;
    let i = n;
    function h() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Fe(l, u), r && u.classList.add(...r.split(" ")), o) {
        const p = Ae(o);
        Object.keys(p).forEach((_) => {
          u.style[_] = p[_];
        });
      }
    }
    let a = null;
    if (e && window.MutationObserver) {
      let u = function() {
        var g, b, I;
        (g = t.current) != null && g.contains(i) && ((b = t.current) == null || b.removeChild(i));
        const {
          portals: _,
          clonedElement: m
        } = A(n);
        return i = m, c(_), i.style.display = "contents", h(), (I = t.current) == null || I.appendChild(i), _.length > 0;
      };
      u() || (a = new window.MutationObserver(() => {
        u() && (a == null || a.disconnect());
      }), a.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", h(), (f = t.current) == null || f.appendChild(i);
    return () => {
      var u, p;
      i.style.display = "", (u = t.current) != null && u.contains(i) && ((p = t.current) == null || p.removeChild(i)), a == null || a.disconnect();
    };
  }, [n, e, r, o, l]), w.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ne(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function De(n, e = !1) {
  try {
    if (e && !Ne(n))
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
function j(n, e) {
  return k(() => De(n, e), [n, e]);
}
function We(n, e) {
  const r = k(() => w.Children.toArray(n).filter((t) => t.props.node && e === t.props.nodeSlotKey).sort((t, s) => {
    if (t.props.node.slotIndex && s.props.node.slotIndex) {
      const c = v(t.props.node.slotIndex) || 0, i = v(s.props.node.slotIndex) || 0;
      return c - i === 0 && t.props.node.subSlotIndex && s.props.node.subSlotIndex ? (v(t.props.node.subSlotIndex) || 0) - (v(s.props.node.subSlotIndex) || 0) : c - i;
    }
    return 0;
  }).map((t) => t.props.node.target), [n, e]);
  return Le(r);
}
function Z(n, e, r) {
  return n.filter(Boolean).map((o, l) => {
    var i;
    if (typeof o != "object")
      return e != null && e.fallback ? e.fallback(o) : o;
    const t = {
      ...o.props,
      key: ((i = o.props) == null ? void 0 : i.key) ?? (r ? `${r}-${l}` : `${l}`)
    };
    let s = t;
    Object.keys(o.slots).forEach((h) => {
      if (!o.slots[h] || !(o.slots[h] instanceof Element) && !o.slots[h].el)
        return;
      const a = h.split(".");
      a.forEach((m, g) => {
        s[m] || (s[m] = {}), g !== a.length - 1 && (s = t[m]);
      });
      const f = o.slots[h];
      let u, p, _ = (e == null ? void 0 : e.clone) ?? !1;
      f instanceof Element ? u = f : (u = f.el, p = f.callback, _ = f.clone ?? !1), s[a[a.length - 1]] = u ? p ? (...m) => (p(a[a.length - 1], m), /* @__PURE__ */ E.jsx(x, {
        slot: u,
        clone: _
      })) : /* @__PURE__ */ E.jsx(x, {
        slot: u,
        clone: _
      }) : s[a[a.length - 1]], s = t;
    });
    const c = (e == null ? void 0 : e.children) || "children";
    return o[c] && (t[c] = Z(o[c], e, `${l}`)), t;
  });
}
function Be(n, e) {
  return n ? /* @__PURE__ */ E.jsx(x, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function U({
  key: n,
  setSlotParams: e,
  slots: r
}, o) {
  return r[n] ? (...l) => (e(n, l), Be(r[n], {
    clone: !0,
    ...o
  })) : void 0;
}
const ze = Pe(({
  getPopupContainer: n,
  slots: e,
  menuItems: r,
  children: o,
  dropdownRender: l,
  buttonsRender: t,
  setSlotParams: s,
  ...c
}) => {
  var u, p, _;
  const i = j(n), h = j(l), a = j(t), f = We(o, "buttonsRender");
  return /* @__PURE__ */ E.jsx(oe.Button, {
    ...c,
    buttonsRender: f.length ? (...m) => (s("buttonsRender", m), f.map((g, b) => /* @__PURE__ */ E.jsx(x, {
      slot: g
    }, b))) : a,
    menu: {
      ...c.menu,
      items: k(() => {
        var m;
        return ((m = c.menu) == null ? void 0 : m.items) || Z(r, {
          clone: !0
        });
      }, [r, (u = c.menu) == null ? void 0 : u.items]),
      expandIcon: e["menu.expandIcon"] ? U({
        slots: e,
        setSlotParams: s,
        key: "menu.expandIcon"
      }, {
        clone: !0
      }) : (p = c.menu) == null ? void 0 : p.expandIcon,
      overflowedIndicator: e["menu.overflowedIndicator"] ? /* @__PURE__ */ E.jsx(x, {
        slot: e["menu.overflowedIndicator"]
      }) : (_ = c.menu) == null ? void 0 : _.overflowedIndicator
    },
    getPopupContainer: i,
    dropdownRender: e.dropdownRender ? U({
      slots: e,
      setSlotParams: s,
      key: "dropdownRender"
    }) : h,
    children: o
  });
});
export {
  ze as DropdownButton,
  ze as default
};
