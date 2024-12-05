import { g as $, w as R } from "./Index-Cdq19uGn.js";
const b = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Breadcrumb;
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
var te = b, re = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, oe = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(r, t, o) {
  var n, l = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) le.call(t, n) && !se.hasOwnProperty(n) && (l[n] = t[n]);
  if (r && r.defaultProps) for (n in t = r.defaultProps, t) l[n] === void 0 && (l[n] = t[n]);
  return {
    $$typeof: re,
    type: r,
    key: e,
    ref: s,
    props: l,
    _owner: oe.current
  };
}
k.Fragment = ne;
k.jsx = z;
k.jsxs = z;
W.exports = k;
var g = W.exports;
const {
  SvelteComponent: ce,
  assign: L,
  binding_callbacks: T,
  check_outros: ae,
  children: G,
  claim_element: U,
  claim_space: ie,
  component_subscribe: N,
  compute_slots: ue,
  create_slot: de,
  detach: E,
  element: H,
  empty: A,
  exclude_internal_props: D,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: me,
  init: pe,
  insert_hydration: C,
  safe_not_equal: he,
  set_custom_element_data: q,
  space: ge,
  transition_in: x,
  transition_out: P,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function B(r) {
  let t, o;
  const n = (
    /*#slots*/
    r[7].default
  ), l = de(
    n,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = H("svelte-slot"), l && l.c(), this.h();
    },
    l(e) {
      t = U(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = G(t);
      l && l.l(s), s.forEach(E), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      C(e, t, s), l && l.m(t, null), r[9](t), o = !0;
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
      o || (x(l, e), o = !0);
    },
    o(e) {
      P(l, e), o = !1;
    },
    d(e) {
      e && E(t), l && l.d(e), r[9](null);
    }
  };
}
function Re(r) {
  let t, o, n, l, e = (
    /*$$slots*/
    r[4].default && B(r)
  );
  return {
    c() {
      t = H("react-portal-target"), o = ge(), e && e.c(), n = A(), this.h();
    },
    l(s) {
      t = U(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), G(t).forEach(E), o = ie(s), e && e.l(s), n = A(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      C(s, t, a), r[8](t), C(s, o, a), e && e.m(s, a), C(s, n, a), l = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && x(e, 1)) : (e = B(s), e.c(), x(e, 1), e.m(n.parentNode, n)) : e && (me(), P(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(s) {
      l || (x(e), l = !0);
    },
    o(s) {
      P(e), l = !1;
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
function Ce(r, t, o) {
  let n, l, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = ue(e);
  let {
    svelteInit: c
  } = t;
  const p = R(F(t)), u = R();
  N(r, u, (d) => o(0, n = d));
  const f = R();
  N(r, f, (d) => o(1, l = d));
  const i = [], _ = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: h,
    subSlotIndex: w
  } = $() || {}, y = c({
    parent: _,
    props: p,
    target: u,
    slot: f,
    slotKey: m,
    slotIndex: h,
    subSlotIndex: w,
    onDestroy(d) {
      i.push(d);
    }
  });
  ve("$$ms-gr-react-wrapper", y), we(() => {
    p.set(F(t));
  }), ye(() => {
    i.forEach((d) => d());
  });
  function v(d) {
    T[d ? "unshift" : "push"](() => {
      n = d, u.set(n);
    });
  }
  function J(d) {
    T[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  return r.$$set = (d) => {
    o(17, t = L(L({}, t), D(d))), "svelteInit" in d && o(5, c = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, t = D(t), [n, l, u, f, a, c, s, e, v, J];
}
class xe extends ce {
  constructor(t) {
    super(), pe(this, t, Ce, Re, he, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, I = window.ms_globals.tree;
function Se(r) {
  function t(o) {
    const n = R(), l = new xe({
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
          }, a = e.parent ?? I;
          return a.nodes = [...a.nodes, s], M({
            createPortal: O,
            node: I
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== n), M({
              createPortal: O,
              node: I
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
function j(r) {
  const t = [], o = r.cloneNode(!1);
  if (r._reactElement)
    return t.push(O(b.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: b.Children.toArray(r._reactElement.props.children).map((l) => {
        if (b.isValidElement(l) && l.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = j(l.props.el);
          return b.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...b.Children.toArray(l.props.children), ...e]
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
      } = j(e);
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
const S = Y(({
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
    function p() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Oe(l, i), o && i.classList.add(...o.split(" ")), n) {
        const _ = Ie(n);
        Object.keys(_).forEach((m) => {
          i.style[m] = _[m];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var w, y, v;
        (w = e.current) != null && w.contains(c) && ((y = e.current) == null || y.removeChild(c));
        const {
          portals: m,
          clonedElement: h
        } = j(r);
        return c = h, a(m), c.style.display = "contents", p(), (v = e.current) == null || v.appendChild(c), m.length > 0;
      };
      i() || (u = new window.MutationObserver(() => {
        i() && (u == null || u.disconnect());
      }), u.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", p(), (f = e.current) == null || f.appendChild(c);
    return () => {
      var i, _;
      c.style.display = "", (i = e.current) != null && i.contains(c) && ((_ = e.current) == null || _.removeChild(c)), u == null || u.disconnect();
    };
  }, [r, t, o, n, l]), b.createElement("react-child", {
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
    Object.keys(n.slots).forEach((p) => {
      if (!n.slots[p] || !(n.slots[p] instanceof Element) && !n.slots[p].el)
        return;
      const u = p.split(".");
      u.forEach((h, w) => {
        s[h] || (s[h] = {}), w !== u.length - 1 && (s = e[h]);
      });
      const f = n.slots[p];
      let i, _, m = (t == null ? void 0 : t.clone) ?? !1;
      f instanceof Element ? i = f : (i = f.el, _ = f.callback, m = f.clone ?? !1), s[u[u.length - 1]] = i ? _ ? (...h) => (_(u[u.length - 1], h), /* @__PURE__ */ g.jsx(S, {
        slot: i,
        clone: m
      })) : /* @__PURE__ */ g.jsx(S, {
        slot: i,
        clone: m
      }) : s[u[u.length - 1]], s = e;
    });
    const a = (t == null ? void 0 : t.children) || "children";
    return n[a] && (e[a] = V(n[a], t, `${l}`)), e;
  });
}
function Pe(r, t) {
  return r ? /* @__PURE__ */ g.jsx(S, {
    slot: r,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function je({
  key: r,
  setSlotParams: t,
  slots: o
}, n) {
  return o[r] ? (...l) => (t(r, l), Pe(o[r], {
    clone: !0,
    ...n
  })) : void 0;
}
const Te = Se(({
  slots: r,
  items: t,
  slotItems: o,
  setSlotParams: n,
  children: l,
  ...e
}) => /* @__PURE__ */ g.jsxs(g.Fragment, {
  children: [/* @__PURE__ */ g.jsx("div", {
    style: {
      display: "none"
    },
    children: l
  }), /* @__PURE__ */ g.jsx(ee, {
    ...e,
    itemRender: r.itemRender ? je({
      setSlotParams: n,
      slots: r,
      key: "itemRender"
    }, {
      clone: !0
    }) : e.itemRender,
    items: Z(() => t || V(o, {
      clone: !0
    }), [t, o]),
    separator: r.separator ? /* @__PURE__ */ g.jsx(S, {
      slot: r.separator,
      clone: !0
    }) : e.separator
  })]
}));
export {
  Te as Breadcrumb,
  Te as default
};
