import { g as $, w as x } from "./Index-BEYyw_Hg.js";
const w = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Descriptions;
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
var te = w, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, t, s) {
  var o, r = {}, e = null, l = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (o in t) oe.call(t, o) && !le.hasOwnProperty(o) && (r[o] = t[o]);
  if (n && n.defaultProps) for (o in t = n.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: ne,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: se.current
  };
}
I.Fragment = re;
I.jsx = G;
I.jsxs = G;
z.exports = I;
var g = z.exports;
const {
  SvelteComponent: ie,
  assign: L,
  binding_callbacks: T,
  check_outros: ce,
  children: U,
  claim_element: H,
  claim_space: ae,
  component_subscribe: N,
  compute_slots: de,
  create_slot: ue,
  detach: E,
  element: q,
  empty: A,
  exclude_internal_props: D,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: he,
  insert_hydration: C,
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
  let t, s;
  const o = (
    /*#slots*/
    n[7].default
  ), r = ue(
    o,
    n,
    /*$$scope*/
    n[6],
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
      C(e, t, l), r && r.m(t, null), n[9](t), s = !0;
    },
    p(e, l) {
      r && r.p && (!s || l & /*$$scope*/
      64) && we(
        r,
        o,
        e,
        /*$$scope*/
        e[6],
        s ? pe(
          o,
          /*$$scope*/
          e[6],
          l,
          null
        ) : fe(
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
      P(r, e), s = !1;
    },
    d(e) {
      e && E(t), r && r.d(e), n[9](null);
    }
  };
}
function xe(n) {
  let t, s, o, r, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = q("react-portal-target"), s = ge(), e && e.c(), o = A(), this.h();
    },
    l(l) {
      t = H(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(E), s = ae(l), e && e.l(l), o = A(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      C(l, t, c), n[8](t), C(l, s, c), e && e.m(l, c), C(l, o, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && R(e, 1)) : (e = F(l), e.c(), R(e, 1), e.m(o.parentNode, o)) : e && (_e(), P(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(l) {
      r || (R(e), r = !0);
    },
    o(l) {
      P(e), r = !1;
    },
    d(l) {
      l && (E(t), E(s), E(o)), n[8](null), e && e.d(l);
    }
  };
}
function M(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function Ce(n, t, s) {
  let o, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = de(e);
  let {
    svelteInit: i
  } = t;
  const h = x(M(t)), d = x();
  N(n, d, (u) => s(0, o = u));
  const f = x();
  N(n, f, (u) => s(1, r = u));
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
    T[u ? "unshift" : "push"](() => {
      o = u, d.set(o);
    });
  }
  function J(u) {
    T[u ? "unshift" : "push"](() => {
      r = u, f.set(r);
    });
  }
  return n.$$set = (u) => {
    s(17, t = L(L({}, t), D(u))), "svelteInit" in u && s(5, i = u.svelteInit), "$$scope" in u && s(6, l = u.$$scope);
  }, t = D(t), [o, r, d, f, c, i, l, e, v, J];
}
class Re extends ie {
  constructor(t) {
    super(), he(this, t, Ce, xe, me, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, O = window.ms_globals.tree;
function Se(n) {
  function t(s) {
    const o = x(), r = new Re({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? O;
          return c.nodes = [...c.nodes, l], W({
            createPortal: k,
            node: O
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), W({
              createPortal: k,
              node: O
            });
          }), l;
        },
        ...s.props
      }
    });
    return o.set(r), r;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(t);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const o = n[s];
    return typeof o == "number" && !Ie.includes(s) ? t[s] = o + "px" : t[s] = o, t;
  }, {}) : {};
}
function j(n) {
  const t = [], s = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(k(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((r) => {
        if (w.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = j(r.props.el);
          return w.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...w.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      s.addEventListener(c, l, i);
    });
  });
  const o = Array.from(n.childNodes);
  for (let r = 0; r < o.length; r++) {
    const e = o[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = j(e);
      t.push(...c), s.appendChild(l);
    } else e.nodeType === 3 && s.appendChild(e.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function ke(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const S = Y(({
  slot: n,
  clone: t,
  className: s,
  style: o
}, r) => {
  const e = K(), [l, c] = Q([]);
  return X(() => {
    var f;
    if (!e.current || !n)
      return;
    let i = n;
    function h() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(r, a), s && a.classList.add(...s.split(" ")), o) {
        const p = Oe(o);
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
  }, [n, t, s, o, r]), w.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function V(n, t, s) {
  return n.filter(Boolean).map((o, r) => {
    var i;
    if (typeof o != "object")
      return o;
    const e = {
      ...o.props,
      key: ((i = o.props) == null ? void 0 : i.key) ?? (s ? `${s}-${r}` : `${r}`)
    };
    let l = e;
    Object.keys(o.slots).forEach((h) => {
      if (!o.slots[h] || !(o.slots[h] instanceof Element) && !o.slots[h].el)
        return;
      const d = h.split(".");
      d.forEach((m, b) => {
        l[m] || (l[m] = {}), b !== d.length - 1 && (l = e[m]);
      });
      const f = o.slots[h];
      let a, p, _ = !1;
      f instanceof Element ? a = f : (a = f.el, p = f.callback, _ = f.clone ?? !1), l[d[d.length - 1]] = a ? p ? (...m) => (p(d[d.length - 1], m), /* @__PURE__ */ g.jsx(S, {
        slot: a,
        clone: _
      })) : /* @__PURE__ */ g.jsx(S, {
        slot: a,
        clone: _
      }) : l[d[d.length - 1]], l = e;
    });
    const c = "children";
    return o[c] && (e[c] = V(o[c], t, `${r}`)), e;
  });
}
const je = Se(({
  slots: n,
  items: t,
  slotItems: s,
  children: o,
  ...r
}) => /* @__PURE__ */ g.jsxs(g.Fragment, {
  children: [/* @__PURE__ */ g.jsx("div", {
    style: {
      display: "none"
    },
    children: o
  }), /* @__PURE__ */ g.jsx(ee, {
    ...r,
    extra: n.extra ? /* @__PURE__ */ g.jsx(S, {
      slot: n.extra
    }) : r.extra,
    title: n.title ? /* @__PURE__ */ g.jsx(S, {
      slot: n.title
    }) : r.title,
    items: Z(() => t || V(s), [t, s])
  })]
}));
export {
  je as Descriptions,
  je as default
};
