import { g as $, w as S } from "./Index-Ceu4i1AD.js";
const g = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Segmented;
var z = {
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
var te = g, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(r, t, o) {
  var n, l = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) le.call(t, n) && !oe.hasOwnProperty(n) && (l[n] = t[n]);
  if (r && r.defaultProps) for (n in t = r.defaultProps, t) l[n] === void 0 && (l[n] = t[n]);
  return {
    $$typeof: ne,
    type: r,
    key: e,
    ref: s,
    props: l,
    _owner: se.current
  };
}
R.Fragment = re;
R.jsx = G;
R.jsxs = G;
z.exports = R;
var w = z.exports;
const {
  SvelteComponent: ce,
  assign: j,
  binding_callbacks: L,
  check_outros: ae,
  children: U,
  claim_element: H,
  claim_space: ie,
  component_subscribe: T,
  compute_slots: de,
  create_slot: ue,
  detach: E,
  element: q,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: he,
  insert_hydration: x,
  safe_not_equal: me,
  set_custom_element_data: B,
  space: ge,
  transition_in: C,
  transition_out: O,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function D(r) {
  let t, o;
  const n = (
    /*#slots*/
    r[7].default
  ), l = ue(
    n,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = q("svelte-slot"), l && l.c(), this.h();
    },
    l(e) {
      t = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = U(t);
      l && l.l(s), s.forEach(E), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      x(e, t, s), l && l.m(t, null), r[9](t), o = !0;
    },
    p(e, s) {
      l && l.p && (!o || s & /*$$scope*/
      64) && be(
        l,
        n,
        e,
        /*$$scope*/
        e[6],
        o ? _e(
          n,
          /*$$scope*/
          e[6],
          s,
          null
        ) : fe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (C(l, e), o = !0);
    },
    o(e) {
      O(l, e), o = !1;
    },
    d(e) {
      e && E(t), l && l.d(e), r[9](null);
    }
  };
}
function Se(r) {
  let t, o, n, l, e = (
    /*$$slots*/
    r[4].default && D(r)
  );
  return {
    c() {
      t = q("react-portal-target"), o = ge(), e && e.c(), n = N(), this.h();
    },
    l(s) {
      t = H(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(E), o = ie(s), e && e.l(s), n = N(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      x(s, t, a), r[8](t), x(s, o, a), e && e.m(s, a), x(s, n, a), l = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && C(e, 1)) : (e = D(s), e.c(), C(e, 1), e.m(n.parentNode, n)) : e && (pe(), O(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(s) {
      l || (C(e), l = !0);
    },
    o(s) {
      O(e), l = !1;
    },
    d(s) {
      s && (E(t), E(o), E(n)), r[8](null), e && e.d(s);
    }
  };
}
function F(r) {
  const {
    svelteInit: t,
    ...o
  } = r;
  return o;
}
function xe(r, t, o) {
  let n, l, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = de(e);
  let {
    svelteInit: c
  } = t;
  const h = S(F(t)), d = S();
  T(r, d, (u) => o(0, n = u));
  const f = S();
  T(r, f, (u) => o(1, l = u));
  const i = [], _ = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: m,
    subSlotIndex: b
  } = $() || {}, y = c({
    parent: _,
    props: h,
    target: d,
    slot: f,
    slotKey: p,
    slotIndex: m,
    subSlotIndex: b,
    onDestroy(u) {
      i.push(u);
    }
  });
  ve("$$ms-gr-react-wrapper", y), we(() => {
    h.set(F(t));
  }), ye(() => {
    i.forEach((u) => u());
  });
  function v(u) {
    L[u ? "unshift" : "push"](() => {
      n = u, d.set(n);
    });
  }
  function J(u) {
    L[u ? "unshift" : "push"](() => {
      l = u, f.set(l);
    });
  }
  return r.$$set = (u) => {
    o(17, t = j(j({}, t), A(u))), "svelteInit" in u && o(5, c = u.svelteInit), "$$scope" in u && o(6, s = u.$$scope);
  }, t = A(t), [n, l, d, f, a, c, s, e, v, J];
}
class Ce extends ce {
  constructor(t) {
    super(), he(this, t, xe, Se, me, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, k = window.ms_globals.tree;
function Re(r) {
  function t(o) {
    const n = S(), l = new Ce({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? k;
          return a.nodes = [...a.nodes, s], M({
            createPortal: I,
            node: k
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== n), M({
              createPortal: I,
              node: k
            });
          }), s;
        },
        ...o.props
      }
    });
    return n.set(l), l;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(r) {
  return r ? Object.keys(r).reduce((t, o) => {
    const n = r[o];
    return typeof n == "number" && !ke.includes(o) ? t[o] = n + "px" : t[o] = n, t;
  }, {}) : {};
}
function P(r) {
  const t = [], o = r.cloneNode(!1);
  if (r._reactElement)
    return t.push(I(g.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: g.Children.toArray(r._reactElement.props.children).map((l) => {
        if (g.isValidElement(l) && l.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = P(l.props.el);
          return g.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...g.Children.toArray(l.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(r.getEventListeners()).forEach((l) => {
    r.getEventListeners(l).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      o.addEventListener(a, s, c);
    });
  });
  const n = Array.from(r.childNodes);
  for (let l = 0; l < n.length; l++) {
    const e = n[l];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = P(e);
      t.push(...a), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Oe(r, t) {
  r && (typeof r == "function" ? r(t) : r.current = t);
}
const W = Y(({
  slot: r,
  clone: t,
  className: o,
  style: n
}, l) => {
  const e = K(), [s, a] = Q([]);
  return X(() => {
    var f;
    if (!e.current || !r)
      return;
    let c = r;
    function h() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Oe(l, i), o && i.classList.add(...o.split(" ")), n) {
        const _ = Ie(n);
        Object.keys(_).forEach((p) => {
          i.style[p] = _[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var b, y, v;
        (b = e.current) != null && b.contains(c) && ((y = e.current) == null || y.removeChild(c));
        const {
          portals: p,
          clonedElement: m
        } = P(r);
        return c = m, a(p), c.style.display = "contents", h(), (v = e.current) == null || v.appendChild(c), p.length > 0;
      };
      i() || (d = new window.MutationObserver(() => {
        i() && (d == null || d.disconnect());
      }), d.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", h(), (f = e.current) == null || f.appendChild(c);
    return () => {
      var i, _;
      c.style.display = "", (i = e.current) != null && i.contains(c) && ((_ = e.current) == null || _.removeChild(c)), d == null || d.disconnect();
    };
  }, [r, t, o, n, l]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function V(r, t, o) {
  return r.filter(Boolean).map((n, l) => {
    var c;
    if (typeof n != "object")
      return t != null && t.fallback ? t.fallback(n) : n;
    const e = {
      ...n.props,
      key: ((c = n.props) == null ? void 0 : c.key) ?? (o ? `${o}-${l}` : `${l}`)
    };
    let s = e;
    Object.keys(n.slots).forEach((h) => {
      if (!n.slots[h] || !(n.slots[h] instanceof Element) && !n.slots[h].el)
        return;
      const d = h.split(".");
      d.forEach((m, b) => {
        s[m] || (s[m] = {}), b !== d.length - 1 && (s = e[m]);
      });
      const f = n.slots[h];
      let i, _, p = (t == null ? void 0 : t.clone) ?? !1;
      f instanceof Element ? i = f : (i = f.el, _ = f.callback, p = f.clone ?? !1), s[d[d.length - 1]] = i ? _ ? (...m) => (_(d[d.length - 1], m), /* @__PURE__ */ w.jsx(W, {
        slot: i,
        clone: p
      })) : /* @__PURE__ */ w.jsx(W, {
        slot: i,
        clone: p
      }) : s[d[d.length - 1]], s = e;
    });
    const a = (t == null ? void 0 : t.children) || "children";
    return n[a] && (e[a] = V(n[a], t, `${l}`)), e;
  });
}
const je = Re(({
  slotItems: r,
  options: t,
  onChange: o,
  onValueChange: n,
  children: l,
  ...e
}) => /* @__PURE__ */ w.jsxs(w.Fragment, {
  children: [/* @__PURE__ */ w.jsx("div", {
    style: {
      display: "none"
    },
    children: l
  }), /* @__PURE__ */ w.jsx(ee, {
    ...e,
    onChange: (s) => {
      o == null || o(s), n(s);
    },
    options: Z(() => t || V(r, {
      clone: !0
    }), [t, r])
  })]
}));
export {
  je as Segmented,
  je as default
};
