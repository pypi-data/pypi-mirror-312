import { g as ee, w as C } from "./Index-DVa8Aclg.js";
const g = window.ms_globals.React, G = window.ms_globals.React.useMemo, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Anchor;
var U = {
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
var ne = g, re = Symbol.for("react.element"), se = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(n, t, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) oe.call(t, s) && !ce.hasOwnProperty(s) && (o[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: re,
    type: n,
    key: e,
    ref: l,
    props: o,
    _owner: le.current
  };
}
S.Fragment = se;
S.jsx = H;
S.jsxs = H;
U.exports = S;
var E = U.exports;
const {
  SvelteComponent: ie,
  assign: j,
  binding_callbacks: A,
  check_outros: ae,
  children: q,
  claim_element: B,
  claim_space: ue,
  component_subscribe: L,
  compute_slots: fe,
  create_slot: de,
  detach: b,
  element: V,
  empty: F,
  exclude_internal_props: T,
  get_all_dirty_from_scope: _e,
  get_slot_changes: he,
  group_outros: pe,
  init: me,
  insert_hydration: R,
  safe_not_equal: ge,
  set_custom_element_data: J,
  space: we,
  transition_in: x,
  transition_out: O,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ye,
  onDestroy: ve,
  setContext: Ce
} = window.__gradio__svelte__internal;
function N(n) {
  let t, r;
  const s = (
    /*#slots*/
    n[7].default
  ), o = de(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = V("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = B(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = q(t);
      o && o.l(l), l.forEach(b), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      R(e, t, l), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && be(
        o,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? he(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : _e(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (x(o, e), r = !0);
    },
    o(e) {
      O(o, e), r = !1;
    },
    d(e) {
      e && b(t), o && o.d(e), n[9](null);
    }
  };
}
function Re(n) {
  let t, r, s, o, e = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      t = V("react-portal-target"), r = we(), e && e.c(), s = F(), this.h();
    },
    l(l) {
      t = B(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(t).forEach(b), r = ue(l), e && e.l(l), s = F(), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      R(l, t, c), n[8](t), R(l, r, c), e && e.m(l, c), R(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && x(e, 1)) : (e = N(l), e.c(), x(e, 1), e.m(s.parentNode, s)) : e && (pe(), O(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(l) {
      o || (x(e), o = !0);
    },
    o(l) {
      O(e), o = !1;
    },
    d(l) {
      l && (b(t), b(r), b(s)), n[8](null), e && e.d(l);
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
function xe(n, t, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = fe(e);
  let {
    svelteInit: i
  } = t;
  const p = C(W(t)), u = C();
  L(n, u, (f) => r(0, s = f));
  const d = C();
  L(n, d, (f) => r(1, o = f));
  const a = [], _ = ye("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: m,
    subSlotIndex: w
  } = ee() || {}, y = i({
    parent: _,
    props: p,
    target: u,
    slot: d,
    slotKey: h,
    slotIndex: m,
    subSlotIndex: w,
    onDestroy(f) {
      a.push(f);
    }
  });
  Ce("$$ms-gr-react-wrapper", y), Ee(() => {
    p.set(W(t));
  }), ve(() => {
    a.forEach((f) => f());
  });
  function v(f) {
    A[f ? "unshift" : "push"](() => {
      s = f, u.set(s);
    });
  }
  function K(f) {
    A[f ? "unshift" : "push"](() => {
      o = f, d.set(o);
    });
  }
  return n.$$set = (f) => {
    r(17, t = j(j({}, t), T(f))), "svelteInit" in f && r(5, i = f.svelteInit), "$$scope" in f && r(6, l = f.$$scope);
  }, t = T(t), [s, o, u, d, c, i, l, e, v, K];
}
class Se extends ie {
  constructor(t) {
    super(), me(this, t, xe, Re, ge, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, k = window.ms_globals.tree;
function ke(n) {
  function t(r) {
    const s = C(), o = new Se({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? k;
          return c.nodes = [...c.nodes, l], D({
            createPortal: I,
            node: k
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), D({
              createPortal: I,
              node: k
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(o), o;
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
function M(n, t) {
  return G(() => Oe(n, t), [n, t]);
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const s = n[r];
    return typeof s == "number" && !Pe.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function P(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(I(g.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: g.Children.toArray(n._reactElement.props.children).map((o) => {
        if (g.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = P(o.props.el);
          return g.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...g.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let o = 0; o < s.length; o++) {
    const e = s[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = P(e);
      t.push(...c), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Ae(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const z = Q(({
  slot: n,
  clone: t,
  className: r,
  style: s
}, o) => {
  const e = X(), [l, c] = Z([]);
  return $(() => {
    var d;
    if (!e.current || !n)
      return;
    let i = n;
    function p() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ae(o, a), r && a.classList.add(...r.split(" ")), s) {
        const _ = je(s);
        Object.keys(_).forEach((h) => {
          a.style[h] = _[h];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var w, y, v;
        (w = e.current) != null && w.contains(i) && ((y = e.current) == null || y.removeChild(i));
        const {
          portals: h,
          clonedElement: m
        } = P(n);
        return i = m, c(h), i.style.display = "contents", p(), (v = e.current) == null || v.appendChild(i), h.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", p(), (d = e.current) == null || d.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((_ = e.current) == null || _.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, t, r, s, o]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Y(n, t, r) {
  return n.filter(Boolean).map((s, o) => {
    var i;
    if (typeof s != "object")
      return t != null && t.fallback ? t.fallback(s) : s;
    const e = {
      ...s.props,
      key: ((i = s.props) == null ? void 0 : i.key) ?? (r ? `${r}-${o}` : `${o}`)
    };
    let l = e;
    Object.keys(s.slots).forEach((p) => {
      if (!s.slots[p] || !(s.slots[p] instanceof Element) && !s.slots[p].el)
        return;
      const u = p.split(".");
      u.forEach((m, w) => {
        l[m] || (l[m] = {}), w !== u.length - 1 && (l = e[m]);
      });
      const d = s.slots[p];
      let a, _, h = (t == null ? void 0 : t.clone) ?? !1;
      d instanceof Element ? a = d : (a = d.el, _ = d.callback, h = d.clone ?? !1), l[u[u.length - 1]] = a ? _ ? (...m) => (_(u[u.length - 1], m), /* @__PURE__ */ E.jsx(z, {
        slot: a,
        clone: h
      })) : /* @__PURE__ */ E.jsx(z, {
        slot: a,
        clone: h
      }) : l[u[u.length - 1]], l = e;
    });
    const c = (t == null ? void 0 : t.children) || "children";
    return s[c] && (e[c] = Y(s[c], t, `${o}`)), e;
  });
}
const Fe = ke(({
  getContainer: n,
  getCurrentAnchor: t,
  children: r,
  items: s,
  slotItems: o,
  ...e
}) => {
  const l = M(n), c = M(t);
  return /* @__PURE__ */ E.jsxs(E.Fragment, {
    children: [r, /* @__PURE__ */ E.jsx(te, {
      ...e,
      items: G(() => s || Y(o, {
        clone: !0
      }), [s, o]),
      getContainer: l,
      getCurrentAnchor: c
    })]
  });
});
export {
  Fe as Anchor,
  Fe as default
};
