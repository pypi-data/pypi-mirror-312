import { g as $, w as x } from "./Index-117Y9LJl.js";
const g = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.internalContext.FormItemContext, te = window.ms_globals.antd.Radio;
var W = {
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
var ne = g, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(o, t, s) {
  var n, r = {}, e = null, l = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (n in t) le.call(t, n) && !ie.hasOwnProperty(n) && (r[n] = t[n]);
  if (o && o.defaultProps) for (n in t = o.defaultProps, t) r[n] === void 0 && (r[n] = t[n]);
  return {
    $$typeof: re,
    type: o,
    key: e,
    ref: l,
    props: r,
    _owner: se.current
  };
}
I.Fragment = oe;
I.jsx = z;
I.jsxs = z;
W.exports = I;
var b = W.exports;
const {
  SvelteComponent: ce,
  assign: j,
  binding_callbacks: L,
  check_outros: ae,
  children: U,
  claim_element: H,
  claim_space: ue,
  component_subscribe: T,
  compute_slots: de,
  create_slot: fe,
  detach: E,
  element: q,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: C,
  safe_not_equal: ge,
  set_custom_element_data: B,
  space: we,
  transition_in: R,
  transition_out: k,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ye,
  onDestroy: ve,
  setContext: xe
} = window.__gradio__svelte__internal;
function F(o) {
  let t, s;
  const n = (
    /*#slots*/
    o[7].default
  ), r = fe(
    n,
    o,
    /*$$scope*/
    o[6],
    null
  );
  return {
    c() {
      t = q("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = U(t);
      r && r.l(l), l.forEach(E), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      C(e, t, l), r && r.m(t, null), o[9](t), s = !0;
    },
    p(e, l) {
      r && r.p && (!s || l & /*$$scope*/
      64) && be(
        r,
        n,
        e,
        /*$$scope*/
        e[6],
        s ? _e(
          n,
          /*$$scope*/
          e[6],
          l,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (R(r, e), s = !0);
    },
    o(e) {
      k(r, e), s = !1;
    },
    d(e) {
      e && E(t), r && r.d(e), o[9](null);
    }
  };
}
function Ce(o) {
  let t, s, n, r, e = (
    /*$$slots*/
    o[4].default && F(o)
  );
  return {
    c() {
      t = q("react-portal-target"), s = we(), e && e.c(), n = N(), this.h();
    },
    l(l) {
      t = H(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(E), s = ue(l), e && e.l(l), n = N(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      C(l, t, i), o[8](t), C(l, s, i), e && e.m(l, i), C(l, n, i), r = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, i), i & /*$$slots*/
      16 && R(e, 1)) : (e = F(l), e.c(), R(e, 1), e.m(n.parentNode, n)) : e && (me(), k(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(l) {
      r || (R(e), r = !0);
    },
    o(l) {
      k(e), r = !1;
    },
    d(l) {
      l && (E(t), E(s), E(n)), o[8](null), e && e.d(l);
    }
  };
}
function D(o) {
  const {
    svelteInit: t,
    ...s
  } = o;
  return s;
}
function Re(o, t, s) {
  let n, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const i = de(e);
  let {
    svelteInit: c
  } = t;
  const m = x(D(t)), u = x();
  T(o, u, (d) => s(0, n = d));
  const f = x();
  T(o, f, (d) => s(1, r = d));
  const a = [], p = ye("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: h,
    subSlotIndex: w
  } = $() || {}, y = c({
    parent: p,
    props: m,
    target: u,
    slot: f,
    slotKey: _,
    slotIndex: h,
    subSlotIndex: w,
    onDestroy(d) {
      a.push(d);
    }
  });
  xe("$$ms-gr-react-wrapper", y), Ee(() => {
    m.set(D(t));
  }), ve(() => {
    a.forEach((d) => d());
  });
  function v(d) {
    L[d ? "unshift" : "push"](() => {
      n = d, u.set(n);
    });
  }
  function J(d) {
    L[d ? "unshift" : "push"](() => {
      r = d, f.set(r);
    });
  }
  return o.$$set = (d) => {
    s(17, t = j(j({}, t), A(d))), "svelteInit" in d && s(5, c = d.svelteInit), "$$scope" in d && s(6, l = d.$$scope);
  }, t = A(t), [n, r, u, f, i, c, l, e, v, J];
}
class Ie extends ce {
  constructor(t) {
    super(), he(this, t, Re, Ce, ge, {
      svelteInit: 5
    });
  }
}
const G = window.ms_globals.rerender, S = window.ms_globals.tree;
function Se(o) {
  function t(s) {
    const n = x(), r = new Ie({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: o,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? S;
          return i.nodes = [...i.nodes, l], G({
            createPortal: O,
            node: S
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== n), G({
              createPortal: O,
              node: S
            });
          }), l;
        },
        ...s.props
      }
    });
    return n.set(r), r;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(t);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(o) {
  return o ? Object.keys(o).reduce((t, s) => {
    const n = o[s];
    return typeof n == "number" && !Oe.includes(s) ? t[s] = n + "px" : t[s] = n, t;
  }, {}) : {};
}
function P(o) {
  const t = [], s = o.cloneNode(!1);
  if (o._reactElement)
    return t.push(O(g.cloneElement(o._reactElement, {
      ...o._reactElement.props,
      children: g.Children.toArray(o._reactElement.props.children).map((r) => {
        if (g.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = P(r.props.el);
          return g.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...g.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: t
    };
  Object.keys(o.getEventListeners()).forEach((r) => {
    o.getEventListeners(r).forEach(({
      listener: l,
      type: i,
      useCapture: c
    }) => {
      s.addEventListener(i, l, c);
    });
  });
  const n = Array.from(o.childNodes);
  for (let r = 0; r < n.length; r++) {
    const e = n[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = P(e);
      t.push(...i), s.appendChild(l);
    } else e.nodeType === 3 && s.appendChild(e.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function Pe(o, t) {
  o && (typeof o == "function" ? o(t) : o.current = t);
}
const M = Y(({
  slot: o,
  clone: t,
  className: s,
  style: n
}, r) => {
  const e = K(), [l, i] = Q([]);
  return X(() => {
    var f;
    if (!e.current || !o)
      return;
    let c = o;
    function m() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Pe(r, a), s && a.classList.add(...s.split(" ")), n) {
        const p = ke(n);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var w, y, v;
        (w = e.current) != null && w.contains(c) && ((y = e.current) == null || y.removeChild(c));
        const {
          portals: _,
          clonedElement: h
        } = P(o);
        return c = h, i(_), c.style.display = "contents", m(), (v = e.current) == null || v.appendChild(c), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(o, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", m(), (f = e.current) == null || f.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = e.current) != null && a.contains(c) && ((p = e.current) == null || p.removeChild(c)), u == null || u.disconnect();
    };
  }, [o, t, s, n, r]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function V(o, t, s) {
  return o.filter(Boolean).map((n, r) => {
    var c;
    if (typeof n != "object")
      return n;
    const e = {
      ...n.props,
      key: ((c = n.props) == null ? void 0 : c.key) ?? (s ? `${s}-${r}` : `${r}`)
    };
    let l = e;
    Object.keys(n.slots).forEach((m) => {
      if (!n.slots[m] || !(n.slots[m] instanceof Element) && !n.slots[m].el)
        return;
      const u = m.split(".");
      u.forEach((h, w) => {
        l[h] || (l[h] = {}), w !== u.length - 1 && (l = e[h]);
      });
      const f = n.slots[m];
      let a, p, _ = !1;
      f instanceof Element ? a = f : (a = f.el, p = f.callback, _ = f.clone ?? !1), l[u[u.length - 1]] = a ? p ? (...h) => (p(u[u.length - 1], h), /* @__PURE__ */ b.jsx(M, {
        slot: a,
        clone: _
      })) : /* @__PURE__ */ b.jsx(M, {
        slot: a,
        clone: _
      }) : l[u[u.length - 1]], l = e;
    });
    const i = "children";
    return n[i] && (e[i] = V(n[i], t, `${r}`)), e;
  });
}
const Le = Se(({
  onValueChange: o,
  onChange: t,
  elRef: s,
  optionItems: n,
  options: r,
  children: e,
  ...l
}) => /* @__PURE__ */ b.jsx(b.Fragment, {
  children: /* @__PURE__ */ b.jsx(te.Group, {
    ...l,
    ref: s,
    options: Z(() => r || V(n), [n, r]),
    onChange: (i) => {
      t == null || t(i), o(i.target.value);
    },
    children: /* @__PURE__ */ b.jsx(ee.Provider, {
      value: null,
      children: e
    })
  })
}));
export {
  Le as RadioGroup,
  Le as default
};
