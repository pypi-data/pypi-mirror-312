import { g as $, w as x } from "./Index-n5L9NeeB.js";
const g = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Checkbox;
var W = {
  exports: {}
}, k = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = g, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(o, t, l) {
  var n, r = {}, e = null, s = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) oe.call(t, n) && !le.hasOwnProperty(n) && (r[n] = t[n]);
  if (o && o.defaultProps) for (n in t = o.defaultProps, t) r[n] === void 0 && (r[n] = t[n]);
  return {
    $$typeof: ne,
    type: o,
    key: e,
    ref: s,
    props: r,
    _owner: se.current
  };
}
k.Fragment = re;
k.jsx = z;
k.jsxs = z;
W.exports = k;
var w = W.exports;
const {
  SvelteComponent: ce,
  assign: j,
  binding_callbacks: L,
  check_outros: ie,
  children: U,
  claim_element: H,
  claim_space: ae,
  component_subscribe: T,
  compute_slots: ue,
  create_slot: de,
  detach: E,
  element: q,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: he,
  insert_hydration: C,
  safe_not_equal: me,
  set_custom_element_data: B,
  space: ge,
  transition_in: R,
  transition_out: O,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function D(o) {
  let t, l;
  const n = (
    /*#slots*/
    o[7].default
  ), r = de(
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
      var s = U(t);
      r && r.l(s), s.forEach(E), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      C(e, t, s), r && r.m(t, null), o[9](t), l = !0;
    },
    p(e, s) {
      r && r.p && (!l || s & /*$$scope*/
      64) && be(
        r,
        n,
        e,
        /*$$scope*/
        e[6],
        l ? pe(
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
      l || (R(r, e), l = !0);
    },
    o(e) {
      O(r, e), l = !1;
    },
    d(e) {
      e && E(t), r && r.d(e), o[9](null);
    }
  };
}
function xe(o) {
  let t, l, n, r, e = (
    /*$$slots*/
    o[4].default && D(o)
  );
  return {
    c() {
      t = q("react-portal-target"), l = ge(), e && e.c(), n = N(), this.h();
    },
    l(s) {
      t = H(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(E), l = ae(s), e && e.l(s), n = N(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      C(s, t, c), o[8](t), C(s, l, c), e && e.m(s, c), C(s, n, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && R(e, 1)) : (e = D(s), e.c(), R(e, 1), e.m(n.parentNode, n)) : e && (_e(), O(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(s) {
      r || (R(e), r = !0);
    },
    o(s) {
      O(e), r = !1;
    },
    d(s) {
      s && (E(t), E(l), E(n)), o[8](null), e && e.d(s);
    }
  };
}
function G(o) {
  const {
    svelteInit: t,
    ...l
  } = o;
  return l;
}
function Ce(o, t, l) {
  let n, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ue(e);
  let {
    svelteInit: i
  } = t;
  const h = x(G(t)), u = x();
  T(o, u, (d) => l(0, n = d));
  const f = x();
  T(o, f, (d) => l(1, r = d));
  const a = [], p = Ee("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: m,
    subSlotIndex: b
  } = $() || {}, y = i({
    parent: p,
    props: h,
    target: u,
    slot: f,
    slotKey: _,
    slotIndex: m,
    subSlotIndex: b,
    onDestroy(d) {
      a.push(d);
    }
  });
  ve("$$ms-gr-react-wrapper", y), we(() => {
    h.set(G(t));
  }), ye(() => {
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
    l(17, t = j(j({}, t), A(d))), "svelteInit" in d && l(5, i = d.svelteInit), "$$scope" in d && l(6, s = d.$$scope);
  }, t = A(t), [n, r, u, f, c, i, s, e, v, J];
}
class Re extends ce {
  constructor(t) {
    super(), he(this, t, Ce, xe, me, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, S = window.ms_globals.tree;
function ke(o) {
  function t(l) {
    const n = x(), r = new Re({
      ...l,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
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
          }, c = e.parent ?? S;
          return c.nodes = [...c.nodes, s], F({
            createPortal: I,
            node: S
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== n), F({
              createPortal: I,
              node: S
            });
          }), s;
        },
        ...l.props
      }
    });
    return n.set(r), r;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(o) {
  return o ? Object.keys(o).reduce((t, l) => {
    const n = o[l];
    return typeof n == "number" && !Se.includes(l) ? t[l] = n + "px" : t[l] = n, t;
  }, {}) : {};
}
function P(o) {
  const t = [], l = o.cloneNode(!1);
  if (o._reactElement)
    return t.push(I(g.cloneElement(o._reactElement, {
      ...o._reactElement.props,
      children: g.Children.toArray(o._reactElement.props.children).map((r) => {
        if (g.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = P(r.props.el);
          return g.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...g.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), l)), {
      clonedElement: l,
      portals: t
    };
  Object.keys(o.getEventListeners()).forEach((r) => {
    o.getEventListeners(r).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      l.addEventListener(c, s, i);
    });
  });
  const n = Array.from(o.childNodes);
  for (let r = 0; r < n.length; r++) {
    const e = n[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = P(e);
      t.push(...c), l.appendChild(s);
    } else e.nodeType === 3 && l.appendChild(e.cloneNode());
  }
  return {
    clonedElement: l,
    portals: t
  };
}
function Oe(o, t) {
  o && (typeof o == "function" ? o(t) : o.current = t);
}
const M = Y(({
  slot: o,
  clone: t,
  className: l,
  style: n
}, r) => {
  const e = K(), [s, c] = Q([]);
  return X(() => {
    var f;
    if (!e.current || !o)
      return;
    let i = o;
    function h() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Oe(r, a), l && a.classList.add(...l.split(" ")), n) {
        const p = Ie(n);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var b, y, v;
        (b = e.current) != null && b.contains(i) && ((y = e.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: m
        } = P(o);
        return i = m, c(_), i.style.display = "contents", h(), (v = e.current) == null || v.appendChild(i), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(o, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", h(), (f = e.current) == null || f.appendChild(i);
    return () => {
      var a, p;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((p = e.current) == null || p.removeChild(i)), u == null || u.disconnect();
    };
  }, [o, t, l, n, r]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function V(o, t, l) {
  return o.filter(Boolean).map((n, r) => {
    var i;
    if (typeof n != "object")
      return n;
    const e = {
      ...n.props,
      key: ((i = n.props) == null ? void 0 : i.key) ?? (l ? `${l}-${r}` : `${r}`)
    };
    let s = e;
    Object.keys(n.slots).forEach((h) => {
      if (!n.slots[h] || !(n.slots[h] instanceof Element) && !n.slots[h].el)
        return;
      const u = h.split(".");
      u.forEach((m, b) => {
        s[m] || (s[m] = {}), b !== u.length - 1 && (s = e[m]);
      });
      const f = n.slots[h];
      let a, p, _ = !1;
      f instanceof Element ? a = f : (a = f.el, p = f.callback, _ = f.clone ?? !1), s[u[u.length - 1]] = a ? p ? (...m) => (p(u[u.length - 1], m), /* @__PURE__ */ w.jsx(M, {
        slot: a,
        clone: _
      })) : /* @__PURE__ */ w.jsx(M, {
        slot: a,
        clone: _
      }) : s[u[u.length - 1]], s = e;
    });
    const c = "children";
    return n[c] && (e[c] = V(n[c], t, `${r}`)), e;
  });
}
const je = ke(({
  onValueChange: o,
  onChange: t,
  elRef: l,
  optionItems: n,
  options: r,
  children: e,
  ...s
}) => /* @__PURE__ */ w.jsxs(w.Fragment, {
  children: [/* @__PURE__ */ w.jsx("div", {
    style: {
      display: "none"
    },
    children: e
  }), /* @__PURE__ */ w.jsx(ee.Group, {
    ...s,
    ref: l,
    options: Z(() => r || V(n), [n, r]),
    onChange: (c) => {
      t == null || t(c), o(c);
    }
  })]
}));
export {
  je as CheckboxGroup,
  je as default
};
