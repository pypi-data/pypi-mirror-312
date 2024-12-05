import { g as $, w as C } from "./Index-D56-jhh-.js";
const w = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Timeline;
var z = {
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
var te = w, ne = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, le = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, t, l) {
  var r, o = {}, e = null, s = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (r in t) re.call(t, r) && !se.hasOwnProperty(r) && (o[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: ne,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: le.current
  };
}
I.Fragment = oe;
I.jsx = G;
I.jsxs = G;
z.exports = I;
var g = z.exports;
const {
  SvelteComponent: ie,
  assign: T,
  binding_callbacks: L,
  check_outros: ce,
  children: U,
  claim_element: H,
  claim_space: ae,
  component_subscribe: D,
  compute_slots: de,
  create_slot: ue,
  detach: E,
  element: q,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: he,
  insert_hydration: x,
  safe_not_equal: me,
  set_custom_element_data: B,
  space: ge,
  transition_in: R,
  transition_out: P,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function F(n) {
  let t, l;
  const r = (
    /*#slots*/
    n[7].default
  ), o = ue(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = q("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = U(t);
      o && o.l(s), s.forEach(E), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      x(e, t, s), o && o.m(t, null), n[9](t), l = !0;
    },
    p(e, s) {
      o && o.p && (!l || s & /*$$scope*/
      64) && we(
        o,
        r,
        e,
        /*$$scope*/
        e[6],
        l ? pe(
          r,
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
      l || (R(o, e), l = !0);
    },
    o(e) {
      P(o, e), l = !1;
    },
    d(e) {
      e && E(t), o && o.d(e), n[9](null);
    }
  };
}
function Ce(n) {
  let t, l, r, o, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = q("react-portal-target"), l = ge(), e && e.c(), r = N(), this.h();
    },
    l(s) {
      t = H(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(E), l = ae(s), e && e.l(s), r = N(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      x(s, t, c), n[8](t), x(s, l, c), e && e.m(s, c), x(s, r, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && R(e, 1)) : (e = F(s), e.c(), R(e, 1), e.m(r.parentNode, r)) : e && (_e(), P(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      o || (R(e), o = !0);
    },
    o(s) {
      P(e), o = !1;
    },
    d(s) {
      s && (E(t), E(l), E(r)), n[8](null), e && e.d(s);
    }
  };
}
function M(n) {
  const {
    svelteInit: t,
    ...l
  } = n;
  return l;
}
function xe(n, t, l) {
  let r, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = de(e);
  let {
    svelteInit: i
  } = t;
  const h = C(M(t)), d = C();
  D(n, d, (u) => l(0, r = u));
  const f = C();
  D(n, f, (u) => l(1, o = u));
  const a = [], p = Ee("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: m,
    subSlotIndex: b
  } = $() || {}, y = i({
    parent: p,
    props: h,
    target: d,
    slot: f,
    slotKey: _,
    slotIndex: m,
    subSlotIndex: b,
    onDestroy(u) {
      a.push(u);
    }
  });
  ve("$$ms-gr-react-wrapper", y), be(() => {
    h.set(M(t));
  }), ye(() => {
    a.forEach((u) => u());
  });
  function v(u) {
    L[u ? "unshift" : "push"](() => {
      r = u, d.set(r);
    });
  }
  function J(u) {
    L[u ? "unshift" : "push"](() => {
      o = u, f.set(o);
    });
  }
  return n.$$set = (u) => {
    l(17, t = T(T({}, t), A(u))), "svelteInit" in u && l(5, i = u.svelteInit), "$$scope" in u && l(6, s = u.$$scope);
  }, t = A(t), [r, o, d, f, c, i, s, e, v, J];
}
class Re extends ie {
  constructor(t) {
    super(), he(this, t, xe, Ce, me, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, O = window.ms_globals.tree;
function Se(n) {
  function t(l) {
    const r = C(), o = new Re({
      ...l,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? O;
          return c.nodes = [...c.nodes, s], W({
            createPortal: k,
            node: O
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== r), W({
              createPortal: k,
              node: O
            });
          }), s;
        },
        ...l.props
      }
    });
    return r.set(o), o;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(n) {
  return n ? Object.keys(n).reduce((t, l) => {
    const r = n[l];
    return typeof r == "number" && !Ie.includes(l) ? t[l] = r + "px" : t[l] = r, t;
  }, {}) : {};
}
function j(n) {
  const t = [], l = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(k(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((o) => {
        if (w.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = j(o.props.el);
          return w.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...w.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), l)), {
      clonedElement: l,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      l.addEventListener(c, s, i);
    });
  });
  const r = Array.from(n.childNodes);
  for (let o = 0; o < r.length; o++) {
    const e = r[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = j(e);
      t.push(...c), l.appendChild(s);
    } else e.nodeType === 3 && l.appendChild(e.cloneNode());
  }
  return {
    clonedElement: l,
    portals: t
  };
}
function ke(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const S = Y(({
  slot: n,
  clone: t,
  className: l,
  style: r
}, o) => {
  const e = K(), [s, c] = Q([]);
  return X(() => {
    var f;
    if (!e.current || !n)
      return;
    let i = n;
    function h() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(o, a), l && a.classList.add(...l.split(" ")), r) {
        const p = Oe(r);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var b, y, v;
        (b = e.current) != null && b.contains(i) && ((y = e.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: m
        } = j(n);
        return i = m, c(_), i.style.display = "contents", h(), (v = e.current) == null || v.appendChild(i), _.length > 0;
      };
      a() || (d = new window.MutationObserver(() => {
        a() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", h(), (f = e.current) == null || f.appendChild(i);
    return () => {
      var a, p;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((p = e.current) == null || p.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, l, r, o]), w.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function V(n, t, l) {
  return n.filter(Boolean).map((r, o) => {
    var i;
    if (typeof r != "object")
      return r;
    const e = {
      ...r.props,
      key: ((i = r.props) == null ? void 0 : i.key) ?? (l ? `${l}-${o}` : `${o}`)
    };
    let s = e;
    Object.keys(r.slots).forEach((h) => {
      if (!r.slots[h] || !(r.slots[h] instanceof Element) && !r.slots[h].el)
        return;
      const d = h.split(".");
      d.forEach((m, b) => {
        s[m] || (s[m] = {}), b !== d.length - 1 && (s = e[m]);
      });
      const f = r.slots[h];
      let a, p, _ = !1;
      f instanceof Element ? a = f : (a = f.el, p = f.callback, _ = f.clone ?? !1), s[d[d.length - 1]] = a ? p ? (...m) => (p(d[d.length - 1], m), /* @__PURE__ */ g.jsx(S, {
        slot: a,
        clone: _
      })) : /* @__PURE__ */ g.jsx(S, {
        slot: a,
        clone: _
      }) : s[d[d.length - 1]], s = e;
    });
    const c = "children";
    return r[c] && (e[c] = V(r[c], t, `${o}`)), e;
  });
}
const je = Se(({
  slots: n,
  items: t,
  slotItems: l,
  children: r,
  ...o
}) => /* @__PURE__ */ g.jsxs(g.Fragment, {
  children: [/* @__PURE__ */ g.jsx("div", {
    style: {
      display: "none"
    },
    children: r
  }), /* @__PURE__ */ g.jsx(ee, {
    ...o,
    items: Z(() => t || V(l), [t, l]),
    pending: n.pending ? /* @__PURE__ */ g.jsx(S, {
      slot: n.pending
    }) : o.pending,
    pendingDot: n.pendingDot ? /* @__PURE__ */ g.jsx(S, {
      slot: n.pendingDot
    }) : o.pendingDot
  })]
}));
export {
  je as Timeline,
  je as default
};
