import { g as $, w as S } from "./Index-B8frF6ov.js";
const g = window.ms_globals.React, z = window.ms_globals.React.useMemo, K = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, O = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Steps;
var G = {
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
var te = g, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, t, r) {
  var o, s = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (o in t) oe.call(t, o) && !le.hasOwnProperty(o) && (s[o] = t[o]);
  if (n && n.defaultProps) for (o in t = n.defaultProps, t) s[o] === void 0 && (s[o] = t[o]);
  return {
    $$typeof: ne,
    type: n,
    key: e,
    ref: l,
    props: s,
    _owner: se.current
  };
}
R.Fragment = re;
R.jsx = U;
R.jsxs = U;
G.exports = R;
var w = G.exports;
const {
  SvelteComponent: ie,
  assign: L,
  binding_callbacks: T,
  check_outros: ce,
  children: H,
  claim_element: q,
  claim_space: ae,
  component_subscribe: F,
  compute_slots: ue,
  create_slot: de,
  detach: y,
  element: B,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: he,
  insert_hydration: C,
  safe_not_equal: me,
  set_custom_element_data: V,
  space: ge,
  transition_in: x,
  transition_out: k,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function D(n) {
  let t, r;
  const o = (
    /*#slots*/
    n[7].default
  ), s = de(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = B("svelte-slot"), s && s.c(), this.h();
    },
    l(e) {
      t = q(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = H(t);
      s && s.l(l), l.forEach(y), this.h();
    },
    h() {
      V(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      C(e, t, l), s && s.m(t, null), n[9](t), r = !0;
    },
    p(e, l) {
      s && s.p && (!r || l & /*$$scope*/
      64) && we(
        s,
        o,
        e,
        /*$$scope*/
        e[6],
        r ? pe(
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
      r || (x(s, e), r = !0);
    },
    o(e) {
      k(s, e), r = !1;
    },
    d(e) {
      e && y(t), s && s.d(e), n[9](null);
    }
  };
}
function Se(n) {
  let t, r, o, s, e = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      t = B("react-portal-target"), r = ge(), e && e.c(), o = N(), this.h();
    },
    l(l) {
      t = q(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(y), r = ae(l), e && e.l(l), o = N(), this.h();
    },
    h() {
      V(t, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      C(l, t, i), n[8](t), C(l, r, i), e && e.m(l, i), C(l, o, i), s = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, i), i & /*$$slots*/
      16 && x(e, 1)) : (e = D(l), e.c(), x(e, 1), e.m(o.parentNode, o)) : e && (_e(), k(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(l) {
      s || (x(e), s = !0);
    },
    o(l) {
      k(e), s = !1;
    },
    d(l) {
      l && (y(t), y(r), y(o)), n[8](null), e && e.d(l);
    }
  };
}
function W(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Ce(n, t, r) {
  let o, s, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const i = ue(e);
  let {
    svelteInit: c
  } = t;
  const h = S(W(t)), u = S();
  F(n, u, (d) => r(0, o = d));
  const f = S();
  F(n, f, (d) => r(1, s = d));
  const a = [], p = ye("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: m,
    subSlotIndex: b
  } = $() || {}, E = c({
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
  ve("$$ms-gr-react-wrapper", E), be(() => {
    h.set(W(t));
  }), Ee(() => {
    a.forEach((d) => d());
  });
  function v(d) {
    T[d ? "unshift" : "push"](() => {
      o = d, u.set(o);
    });
  }
  function Y(d) {
    T[d ? "unshift" : "push"](() => {
      s = d, f.set(s);
    });
  }
  return n.$$set = (d) => {
    r(17, t = L(L({}, t), A(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, l = d.$$scope);
  }, t = A(t), [o, s, u, f, i, c, l, e, v, Y];
}
class xe extends ie {
  constructor(t) {
    super(), he(this, t, Ce, Se, me, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, I = window.ms_globals.tree;
function Re(n) {
  function t(r) {
    const o = S(), s = new xe({
      ...r,
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
          }, i = e.parent ?? I;
          return i.nodes = [...i.nodes, l], M({
            createPortal: O,
            node: I
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== o), M({
              createPortal: O,
              node: I
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
      r(t);
    });
  });
}
function Ie(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Oe(n, t = !1) {
  try {
    if (t && !Ie(n))
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
function ke(n, t) {
  return z(() => Oe(n, t), [n, t]);
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const o = n[r];
    return typeof o == "number" && !Pe.includes(r) ? t[r] = o + "px" : t[r] = o, t;
  }, {}) : {};
}
function P(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(O(g.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: g.Children.toArray(n._reactElement.props.children).map((s) => {
        if (g.isValidElement(s) && s.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = P(s.props.el);
          return g.cloneElement(s, {
            ...s.props,
            el: l,
            children: [...g.Children.toArray(s.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((s) => {
    n.getEventListeners(s).forEach(({
      listener: l,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, l, c);
    });
  });
  const o = Array.from(n.childNodes);
  for (let s = 0; s < o.length; s++) {
    const e = o[s];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = P(e);
      t.push(...i), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Le(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const j = K(({
  slot: n,
  clone: t,
  className: r,
  style: o
}, s) => {
  const e = Q(), [l, i] = X([]);
  return Z(() => {
    var f;
    if (!e.current || !n)
      return;
    let c = n;
    function h() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Le(s, a), r && a.classList.add(...r.split(" ")), o) {
        const p = je(o);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var b, E, v;
        (b = e.current) != null && b.contains(c) && ((E = e.current) == null || E.removeChild(c));
        const {
          portals: _,
          clonedElement: m
        } = P(n);
        return c = m, i(_), c.style.display = "contents", h(), (v = e.current) == null || v.appendChild(c), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", h(), (f = e.current) == null || f.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = e.current) != null && a.contains(c) && ((p = e.current) == null || p.removeChild(c)), u == null || u.disconnect();
    };
  }, [n, t, r, o, s]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function J(n, t, r) {
  return n.filter(Boolean).map((o, s) => {
    var c;
    if (typeof o != "object")
      return o;
    const e = {
      ...o.props,
      key: ((c = o.props) == null ? void 0 : c.key) ?? (r ? `${r}-${s}` : `${s}`)
    };
    let l = e;
    Object.keys(o.slots).forEach((h) => {
      if (!o.slots[h] || !(o.slots[h] instanceof Element) && !o.slots[h].el)
        return;
      const u = h.split(".");
      u.forEach((m, b) => {
        l[m] || (l[m] = {}), b !== u.length - 1 && (l = e[m]);
      });
      const f = o.slots[h];
      let a, p, _ = !1;
      f instanceof Element ? a = f : (a = f.el, p = f.callback, _ = f.clone ?? !1), l[u[u.length - 1]] = a ? p ? (...m) => (p(u[u.length - 1], m), /* @__PURE__ */ w.jsx(j, {
        slot: a,
        clone: _
      })) : /* @__PURE__ */ w.jsx(j, {
        slot: a,
        clone: _
      }) : l[u[u.length - 1]], l = e;
    });
    const i = "children";
    return o[i] && (e[i] = J(o[i], t, `${s}`)), e;
  });
}
function Te(n, t) {
  return n ? /* @__PURE__ */ w.jsx(j, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Fe({
  key: n,
  setSlotParams: t,
  slots: r
}, o) {
  return r[n] ? (...s) => (t(n, s), Te(r[n], {
    clone: !0,
    ...o
  })) : void 0;
}
const Ae = Re(({
  slots: n,
  items: t,
  slotItems: r,
  setSlotParams: o,
  children: s,
  progressDot: e,
  ...l
}) => {
  const i = ke(e);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: s
    }), /* @__PURE__ */ w.jsx(ee, {
      ...l,
      items: z(() => t || J(r), [t, r]),
      progressDot: n.progressDot ? Fe({
        slots: n,
        setSlotParams: o,
        key: "progressDot"
      }, {
        clone: !0
      }) : i || e
    })]
  });
});
export {
  Ae as Steps,
  Ae as default
};
