import { g as $, w as x } from "./Index-DXVDIf6a.js";
const g = window.ms_globals.React, z = window.ms_globals.React.useMemo, K = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, k = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Collapse;
var G = {
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
var te = g, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, e, r) {
  var l, s = {}, t = null, o = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (o = e.ref);
  for (l in e) le.call(e, l) && !oe.hasOwnProperty(l) && (s[l] = e[l]);
  if (n && n.defaultProps) for (l in e = n.defaultProps, e) s[l] === void 0 && (s[l] = e[l]);
  return {
    $$typeof: ne,
    type: n,
    key: t,
    ref: o,
    props: s,
    _owner: se.current
  };
}
S.Fragment = re;
S.jsx = U;
S.jsxs = U;
G.exports = S;
var E = G.exports;
const {
  SvelteComponent: ce,
  assign: L,
  binding_callbacks: T,
  check_outros: ie,
  children: H,
  claim_element: q,
  claim_space: ae,
  component_subscribe: F,
  compute_slots: ue,
  create_slot: de,
  detach: b,
  element: B,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: he,
  insert_hydration: C,
  safe_not_equal: me,
  set_custom_element_data: V,
  space: ge,
  transition_in: R,
  transition_out: O,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function W(n) {
  let e, r;
  const l = (
    /*#slots*/
    n[7].default
  ), s = de(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = B("svelte-slot"), s && s.c(), this.h();
    },
    l(t) {
      e = q(t, "SVELTE-SLOT", {
        class: !0
      });
      var o = H(e);
      s && s.l(o), o.forEach(b), this.h();
    },
    h() {
      V(e, "class", "svelte-1rt0kpf");
    },
    m(t, o) {
      C(t, e, o), s && s.m(e, null), n[9](e), r = !0;
    },
    p(t, o) {
      s && s.p && (!r || o & /*$$scope*/
      64) && we(
        s,
        l,
        t,
        /*$$scope*/
        t[6],
        r ? _e(
          l,
          /*$$scope*/
          t[6],
          o,
          null
        ) : fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (R(s, t), r = !0);
    },
    o(t) {
      O(s, t), r = !1;
    },
    d(t) {
      t && b(e), s && s.d(t), n[9](null);
    }
  };
}
function xe(n) {
  let e, r, l, s, t = (
    /*$$slots*/
    n[4].default && W(n)
  );
  return {
    c() {
      e = B("react-portal-target"), r = ge(), t && t.c(), l = N(), this.h();
    },
    l(o) {
      e = q(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(e).forEach(b), r = ae(o), t && t.l(o), l = N(), this.h();
    },
    h() {
      V(e, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      C(o, e, i), n[8](e), C(o, r, i), t && t.m(o, i), C(o, l, i), s = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? t ? (t.p(o, i), i & /*$$slots*/
      16 && R(t, 1)) : (t = W(o), t.c(), R(t, 1), t.m(l.parentNode, l)) : t && (pe(), O(t, 1, 1, () => {
        t = null;
      }), ie());
    },
    i(o) {
      s || (R(t), s = !0);
    },
    o(o) {
      O(t), s = !1;
    },
    d(o) {
      o && (b(e), b(r), b(l)), n[8](null), t && t.d(o);
    }
  };
}
function D(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function Ce(n, e, r) {
  let l, s, {
    $$slots: t = {},
    $$scope: o
  } = e;
  const i = ue(t);
  let {
    svelteInit: c
  } = e;
  const f = x(D(e)), u = x();
  F(n, u, (d) => r(0, l = d));
  const _ = x();
  F(n, _, (d) => r(1, s = d));
  const a = [], p = Ee("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: m,
    subSlotIndex: w
  } = $() || {}, y = c({
    parent: p,
    props: f,
    target: u,
    slot: _,
    slotKey: h,
    slotIndex: m,
    subSlotIndex: w,
    onDestroy(d) {
      a.push(d);
    }
  });
  ve("$$ms-gr-react-wrapper", y), be(() => {
    f.set(D(e));
  }), ye(() => {
    a.forEach((d) => d());
  });
  function v(d) {
    T[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function Y(d) {
    T[d ? "unshift" : "push"](() => {
      s = d, _.set(s);
    });
  }
  return n.$$set = (d) => {
    r(17, e = L(L({}, e), A(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, o = d.$$scope);
  }, e = A(e), [l, s, u, _, i, c, o, t, v, Y];
}
class Re extends ce {
  constructor(e) {
    super(), he(this, e, Ce, xe, me, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, I = window.ms_globals.tree;
function Se(n) {
  function e(r) {
    const l = x(), s = new Re({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? I;
          return i.nodes = [...i.nodes, o], M({
            createPortal: k,
            node: I
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), M({
              createPortal: k,
              node: I
            });
          }), o;
        },
        ...r.props
      }
    });
    return l.set(s), s;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(e);
    });
  });
}
function Ie(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function ke(n, e = !1) {
  try {
    if (e && !Ie(n))
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
function Oe(n, e) {
  return z(() => ke(n, e), [n, e]);
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const l = n[r];
    return typeof l == "number" && !Pe.includes(r) ? e[r] = l + "px" : e[r] = l, e;
  }, {}) : {};
}
function P(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(k(g.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: g.Children.toArray(n._reactElement.props.children).map((s) => {
        if (g.isValidElement(s) && s.props.__slot__) {
          const {
            portals: t,
            clonedElement: o
          } = P(s.props.el);
          return g.cloneElement(s, {
            ...s.props,
            el: o,
            children: [...g.Children.toArray(s.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((s) => {
    n.getEventListeners(s).forEach(({
      listener: o,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, o, c);
    });
  });
  const l = Array.from(n.childNodes);
  for (let s = 0; s < l.length; s++) {
    const t = l[s];
    if (t.nodeType === 1) {
      const {
        clonedElement: o,
        portals: i
      } = P(t);
      e.push(...i), r.appendChild(o);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Le(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const j = K(({
  slot: n,
  clone: e,
  className: r,
  style: l
}, s) => {
  const t = Q(), [o, i] = X([]);
  return Z(() => {
    var _;
    if (!t.current || !n)
      return;
    let c = n;
    function f() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Le(s, a), r && a.classList.add(...r.split(" ")), l) {
        const p = je(l);
        Object.keys(p).forEach((h) => {
          a.style[h] = p[h];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var w, y, v;
        (w = t.current) != null && w.contains(c) && ((y = t.current) == null || y.removeChild(c));
        const {
          portals: h,
          clonedElement: m
        } = P(n);
        return c = m, i(h), c.style.display = "contents", f(), (v = t.current) == null || v.appendChild(c), h.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", f(), (_ = t.current) == null || _.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = t.current) != null && a.contains(c) && ((p = t.current) == null || p.removeChild(c)), u == null || u.disconnect();
    };
  }, [n, e, r, l, s]), g.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...o);
});
function J(n, e, r) {
  return n.filter(Boolean).map((l, s) => {
    var c;
    if (typeof l != "object")
      return e != null && e.fallback ? e.fallback(l) : l;
    const t = {
      ...l.props,
      key: ((c = l.props) == null ? void 0 : c.key) ?? (r ? `${r}-${s}` : `${s}`)
    };
    let o = t;
    Object.keys(l.slots).forEach((f) => {
      if (!l.slots[f] || !(l.slots[f] instanceof Element) && !l.slots[f].el)
        return;
      const u = f.split(".");
      u.forEach((m, w) => {
        o[m] || (o[m] = {}), w !== u.length - 1 && (o = t[m]);
      });
      const _ = l.slots[f];
      let a, p, h = (e == null ? void 0 : e.clone) ?? !1;
      _ instanceof Element ? a = _ : (a = _.el, p = _.callback, h = _.clone ?? !1), o[u[u.length - 1]] = a ? p ? (...m) => (p(u[u.length - 1], m), /* @__PURE__ */ E.jsx(j, {
        slot: a,
        clone: h
      })) : /* @__PURE__ */ E.jsx(j, {
        slot: a,
        clone: h
      }) : o[u[u.length - 1]], o = t;
    });
    const i = (e == null ? void 0 : e.children) || "children";
    return l[i] && (t[i] = J(l[i], e, `${s}`)), t;
  });
}
function Te(n, e) {
  return n ? /* @__PURE__ */ E.jsx(j, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Fe({
  key: n,
  setSlotParams: e,
  slots: r
}, l) {
  return r[n] ? (...s) => (e(n, s), Te(r[n], {
    clone: !0,
    ...l
  })) : void 0;
}
const Ae = Se(({
  slots: n,
  items: e,
  slotItems: r,
  children: l,
  onChange: s,
  setSlotParams: t,
  expandIcon: o,
  ...i
}) => {
  const c = Oe(o);
  return /* @__PURE__ */ E.jsxs(E.Fragment, {
    children: [l, /* @__PURE__ */ E.jsx(ee, {
      ...i,
      onChange: (f) => {
        s == null || s(f);
      },
      expandIcon: n.expandIcon ? Fe({
        slots: n,
        setSlotParams: t,
        key: "expandIcon"
      }) : c,
      items: z(() => e || J(r, {
        clone: !0
      }), [e, r])
    })]
  });
});
export {
  Ae as Collapse,
  Ae as default
};
