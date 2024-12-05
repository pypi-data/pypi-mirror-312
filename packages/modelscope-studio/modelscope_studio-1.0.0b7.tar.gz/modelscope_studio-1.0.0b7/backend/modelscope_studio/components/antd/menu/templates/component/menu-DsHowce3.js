import { g as $, w as x } from "./Index-DsJbh_5J.js";
const g = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Menu;
var z = {
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
var te = g, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, oe = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, e, o) {
  var r, l = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (r in e) le.call(e, r) && !se.hasOwnProperty(r) && (l[r] = e[r]);
  if (n && n.defaultProps) for (r in e = n.defaultProps, e) l[r] === void 0 && (l[r] = e[r]);
  return {
    $$typeof: ne,
    type: n,
    key: t,
    ref: s,
    props: l,
    _owner: oe.current
  };
}
S.Fragment = re;
S.jsx = G;
S.jsxs = G;
z.exports = S;
var w = z.exports;
const {
  SvelteComponent: ce,
  assign: L,
  binding_callbacks: T,
  check_outros: ae,
  children: D,
  claim_element: H,
  claim_space: ie,
  component_subscribe: N,
  compute_slots: de,
  create_slot: ue,
  detach: E,
  element: q,
  empty: A,
  exclude_internal_props: M,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: he,
  init: me,
  insert_hydration: I,
  safe_not_equal: pe,
  set_custom_element_data: B,
  space: ge,
  transition_in: C,
  transition_out: P,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: Ee,
  onDestroy: ve,
  setContext: ye
} = window.__gradio__svelte__internal;
function F(n) {
  let e, o;
  const r = (
    /*#slots*/
    n[7].default
  ), l = ue(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = q("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      e = H(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = D(e);
      l && l.l(s), s.forEach(E), this.h();
    },
    h() {
      B(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      I(t, e, s), l && l.m(e, null), n[9](e), o = !0;
    },
    p(t, s) {
      l && l.p && (!o || s & /*$$scope*/
      64) && we(
        l,
        r,
        t,
        /*$$scope*/
        t[6],
        o ? _e(
          r,
          /*$$scope*/
          t[6],
          s,
          null
        ) : fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (C(l, t), o = !0);
    },
    o(t) {
      P(l, t), o = !1;
    },
    d(t) {
      t && E(e), l && l.d(t), n[9](null);
    }
  };
}
function xe(n) {
  let e, o, r, l, t = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      e = q("react-portal-target"), o = ge(), t && t.c(), r = A(), this.h();
    },
    l(s) {
      e = H(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), D(e).forEach(E), o = ie(s), t && t.l(s), r = A(), this.h();
    },
    h() {
      B(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      I(s, e, a), n[8](e), I(s, o, a), t && t.m(s, a), I(s, r, a), l = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, a), a & /*$$slots*/
      16 && C(t, 1)) : (t = F(s), t.c(), C(t, 1), t.m(r.parentNode, r)) : t && (he(), P(t, 1, 1, () => {
        t = null;
      }), ae());
    },
    i(s) {
      l || (C(t), l = !0);
    },
    o(s) {
      P(t), l = !1;
    },
    d(s) {
      s && (E(e), E(o), E(r)), n[8](null), t && t.d(s);
    }
  };
}
function U(n) {
  const {
    svelteInit: e,
    ...o
  } = n;
  return o;
}
function Ie(n, e, o) {
  let r, l, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const a = de(t);
  let {
    svelteInit: c
  } = e;
  const f = x(U(e)), d = x();
  N(n, d, (u) => o(0, r = u));
  const _ = x();
  N(n, _, (u) => o(1, l = u));
  const i = [], h = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: p,
    subSlotIndex: b
  } = $() || {}, v = c({
    parent: h,
    props: f,
    target: d,
    slot: _,
    slotKey: m,
    slotIndex: p,
    subSlotIndex: b,
    onDestroy(u) {
      i.push(u);
    }
  });
  ye("$$ms-gr-react-wrapper", v), be(() => {
    f.set(U(e));
  }), ve(() => {
    i.forEach((u) => u());
  });
  function y(u) {
    T[u ? "unshift" : "push"](() => {
      r = u, d.set(r);
    });
  }
  function J(u) {
    T[u ? "unshift" : "push"](() => {
      l = u, _.set(l);
    });
  }
  return n.$$set = (u) => {
    o(17, e = L(L({}, e), M(u))), "svelteInit" in u && o(5, c = u.svelteInit), "$$scope" in u && o(6, s = u.$$scope);
  }, e = M(e), [r, l, d, _, a, c, s, t, y, J];
}
class Ce extends ce {
  constructor(e) {
    super(), me(this, e, Ie, xe, pe, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, k = window.ms_globals.tree;
function Re(n) {
  function e(o) {
    const r = x(), l = new Ce({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, a = t.parent ?? k;
          return a.nodes = [...a.nodes, s], W({
            createPortal: O,
            node: k
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== r), W({
              createPortal: O,
              node: k
            });
          }), s;
        },
        ...o.props
      }
    });
    return r.set(l), l;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(e);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(n) {
  return n ? Object.keys(n).reduce((e, o) => {
    const r = n[o];
    return typeof r == "number" && !Se.includes(o) ? e[o] = r + "px" : e[o] = r, e;
  }, {}) : {};
}
function j(n) {
  const e = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(O(g.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: g.Children.toArray(n._reactElement.props.children).map((l) => {
        if (g.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = j(l.props.el);
          return g.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...g.Children.toArray(l.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((l) => {
    n.getEventListeners(l).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      o.addEventListener(a, s, c);
    });
  });
  const r = Array.from(n.childNodes);
  for (let l = 0; l < r.length; l++) {
    const t = r[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = j(t);
      e.push(...a), o.appendChild(s);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function Oe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const R = Y(({
  slot: n,
  clone: e,
  className: o,
  style: r
}, l) => {
  const t = K(), [s, a] = Q([]);
  return X(() => {
    var _;
    if (!t.current || !n)
      return;
    let c = n;
    function f() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Oe(l, i), o && i.classList.add(...o.split(" ")), r) {
        const h = ke(r);
        Object.keys(h).forEach((m) => {
          i.style[m] = h[m];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let i = function() {
        var b, v, y;
        (b = t.current) != null && b.contains(c) && ((v = t.current) == null || v.removeChild(c));
        const {
          portals: m,
          clonedElement: p
        } = j(n);
        return c = p, a(m), c.style.display = "contents", f(), (y = t.current) == null || y.appendChild(c), m.length > 0;
      };
      i() || (d = new window.MutationObserver(() => {
        i() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", f(), (_ = t.current) == null || _.appendChild(c);
    return () => {
      var i, h;
      c.style.display = "", (i = t.current) != null && i.contains(c) && ((h = t.current) == null || h.removeChild(c)), d == null || d.disconnect();
    };
  }, [n, e, o, r, l]), g.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Pe(n) {
  return Object.keys(n).reduce((e, o) => (n[o] !== void 0 && (e[o] = n[o]), e), {});
}
function V(n, e, o) {
  return n.filter(Boolean).map((r, l) => {
    var c;
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const t = {
      ...r.props,
      key: ((c = r.props) == null ? void 0 : c.key) ?? (o ? `${o}-${l}` : `${l}`)
    };
    let s = t;
    Object.keys(r.slots).forEach((f) => {
      if (!r.slots[f] || !(r.slots[f] instanceof Element) && !r.slots[f].el)
        return;
      const d = f.split(".");
      d.forEach((p, b) => {
        s[p] || (s[p] = {}), b !== d.length - 1 && (s = t[p]);
      });
      const _ = r.slots[f];
      let i, h, m = (e == null ? void 0 : e.clone) ?? !1;
      _ instanceof Element ? i = _ : (i = _.el, h = _.callback, m = _.clone ?? !1), s[d[d.length - 1]] = i ? h ? (...p) => (h(d[d.length - 1], p), /* @__PURE__ */ w.jsx(R, {
        slot: i,
        clone: m
      })) : /* @__PURE__ */ w.jsx(R, {
        slot: i,
        clone: m
      }) : s[d[d.length - 1]], s = t;
    });
    const a = (e == null ? void 0 : e.children) || "children";
    return r[a] && (t[a] = V(r[a], e, `${l}`)), t;
  });
}
function je(n, e) {
  return n ? /* @__PURE__ */ w.jsx(R, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Le({
  key: n,
  setSlotParams: e,
  slots: o
}, r) {
  return o[n] ? (...l) => (e(n, l), je(o[n], {
    clone: !0,
    ...r
  })) : void 0;
}
const Ne = Re(({
  slots: n,
  items: e,
  slotItems: o,
  children: r,
  onOpenChange: l,
  onSelect: t,
  onDeselect: s,
  setSlotParams: a,
  ...c
}) => /* @__PURE__ */ w.jsxs(w.Fragment, {
  children: [r, /* @__PURE__ */ w.jsx(ee, {
    ...Pe(c),
    onOpenChange: (f) => {
      l == null || l(f);
    },
    onSelect: (f) => {
      t == null || t(f);
    },
    onDeselect: (f) => {
      s == null || s(f);
    },
    items: Z(() => e || V(o, {
      clone: !0
    }), [e, o]),
    expandIcon: n.expandIcon ? Le({
      key: "expandIcon",
      slots: n,
      setSlotParams: a
    }, {
      clone: !0
    }) : c.expandIcon,
    overflowedIndicator: n.overflowedIndicator ? /* @__PURE__ */ w.jsx(R, {
      slot: n.overflowedIndicator
    }) : c.overflowedIndicator
  })]
}));
export {
  Ne as Menu,
  Ne as default
};
