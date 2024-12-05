import { b as ee, g as te, w as C } from "./Index-nvW3kdcP.js";
const w = window.ms_globals.React, $ = window.ms_globals.React.forwardRef, O = window.ms_globals.React.useRef, G = window.ms_globals.React.useState, P = window.ms_globals.React.useEffect, U = window.ms_globals.React.useMemo, j = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.antd.Mentions;
function re(n, e) {
  return ee(n, e);
}
var H = {
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
var se = w, oe = Symbol.for("react.element"), le = Symbol.for("react.fragment"), ce = Object.prototype.hasOwnProperty, ie = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function B(n, e, r) {
  var s, o = {}, t = null, l = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (s in e) ce.call(e, s) && !ae.hasOwnProperty(s) && (o[s] = e[s]);
  if (n && n.defaultProps) for (s in e = n.defaultProps, e) o[s] === void 0 && (o[s] = e[s]);
  return {
    $$typeof: oe,
    type: n,
    key: t,
    ref: l,
    props: o,
    _owner: ie.current
  };
}
S.Fragment = le;
S.jsx = B;
S.jsxs = B;
H.exports = S;
var b = H.exports;
const {
  SvelteComponent: ue,
  assign: N,
  binding_callbacks: A,
  check_outros: de,
  children: J,
  claim_element: Y,
  claim_space: fe,
  component_subscribe: M,
  compute_slots: _e,
  create_slot: pe,
  detach: y,
  element: K,
  empty: V,
  exclude_internal_props: W,
  get_all_dirty_from_scope: he,
  get_slot_changes: me,
  group_outros: ge,
  init: we,
  insert_hydration: R,
  safe_not_equal: be,
  set_custom_element_data: Q,
  space: Ee,
  transition_in: x,
  transition_out: F,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: Ce,
  onDestroy: Re,
  setContext: xe
} = window.__gradio__svelte__internal;
function D(n) {
  let e, r;
  const s = (
    /*#slots*/
    n[7].default
  ), o = pe(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = K("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      e = Y(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = J(e);
      o && o.l(l), l.forEach(y), this.h();
    },
    h() {
      Q(e, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      R(t, e, l), o && o.m(e, null), n[9](e), r = !0;
    },
    p(t, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && ye(
        o,
        s,
        t,
        /*$$scope*/
        t[6],
        r ? me(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : he(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (x(o, t), r = !0);
    },
    o(t) {
      F(o, t), r = !1;
    },
    d(t) {
      t && y(e), o && o.d(t), n[9](null);
    }
  };
}
function Se(n) {
  let e, r, s, o, t = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      e = K("react-portal-target"), r = Ee(), t && t.c(), s = V(), this.h();
    },
    l(l) {
      e = Y(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(e).forEach(y), r = fe(l), t && t.l(l), s = V(), this.h();
    },
    h() {
      Q(e, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      R(l, e, i), n[8](e), R(l, r, i), t && t.m(l, i), R(l, s, i), o = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, i), i & /*$$slots*/
      16 && x(t, 1)) : (t = D(l), t.c(), x(t, 1), t.m(s.parentNode, s)) : t && (ge(), F(t, 1, 1, () => {
        t = null;
      }), de());
    },
    i(l) {
      o || (x(t), o = !0);
    },
    o(l) {
      F(t), o = !1;
    },
    d(l) {
      l && (y(e), y(r), y(s)), n[8](null), t && t.d(l);
    }
  };
}
function q(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function ke(n, e, r) {
  let s, o, {
    $$slots: t = {},
    $$scope: l
  } = e;
  const i = _e(t);
  let {
    svelteInit: c
  } = e;
  const h = C(q(e)), a = C();
  M(n, a, (d) => r(0, s = d));
  const f = C();
  M(n, f, (d) => r(1, o = d));
  const u = [], _ = Ce("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: m,
    subSlotIndex: g
  } = te() || {}, E = c({
    parent: _,
    props: h,
    target: a,
    slot: f,
    slotKey: p,
    slotIndex: m,
    subSlotIndex: g,
    onDestroy(d) {
      u.push(d);
    }
  });
  xe("$$ms-gr-react-wrapper", E), ve(() => {
    h.set(q(e));
  }), Re(() => {
    u.forEach((d) => d());
  });
  function v(d) {
    A[d ? "unshift" : "push"](() => {
      s = d, a.set(s);
    });
  }
  function Z(d) {
    A[d ? "unshift" : "push"](() => {
      o = d, f.set(o);
    });
  }
  return n.$$set = (d) => {
    r(17, e = N(N({}, e), W(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, l = d.$$scope);
  }, e = W(e), [s, o, a, f, i, c, l, t, v, Z];
}
class Ie extends ue {
  constructor(e) {
    super(), we(this, e, ke, Se, be, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, k = window.ms_globals.tree;
function Oe(n) {
  function e(r) {
    const s = C(), o = new Ie({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? k;
          return i.nodes = [...i.nodes, l], z({
            createPortal: j,
            node: k
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), z({
              createPortal: j,
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
      r(e);
    });
  });
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const s = n[r];
    return typeof s == "number" && !Pe.includes(r) ? e[r] = s + "px" : e[r] = s, e;
  }, {}) : {};
}
function L(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(j(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((o) => {
        if (w.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = L(o.props.el);
          return w.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...w.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: l,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, l, c);
    });
  });
  const s = Array.from(n.childNodes);
  for (let o = 0; o < s.length; o++) {
    const t = s[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = L(t);
      e.push(...i), r.appendChild(l);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Fe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const T = $(({
  slot: n,
  clone: e,
  className: r,
  style: s
}, o) => {
  const t = O(), [l, i] = G([]);
  return P(() => {
    var f;
    if (!t.current || !n)
      return;
    let c = n;
    function h() {
      let u = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (u = c.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Fe(o, u), r && u.classList.add(...r.split(" ")), s) {
        const _ = je(s);
        Object.keys(_).forEach((p) => {
          u.style[p] = _[p];
        });
      }
    }
    let a = null;
    if (e && window.MutationObserver) {
      let u = function() {
        var g, E, v;
        (g = t.current) != null && g.contains(c) && ((E = t.current) == null || E.removeChild(c));
        const {
          portals: p,
          clonedElement: m
        } = L(n);
        return c = m, i(p), c.style.display = "contents", h(), (v = t.current) == null || v.appendChild(c), p.length > 0;
      };
      u() || (a = new window.MutationObserver(() => {
        u() && (a == null || a.disconnect());
      }), a.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", h(), (f = t.current) == null || f.appendChild(c);
    return () => {
      var u, _;
      c.style.display = "", (u = t.current) != null && u.contains(c) && ((_ = t.current) == null || _.removeChild(c)), a == null || a.disconnect();
    };
  }, [n, e, r, s, o]), w.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Le(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Te(n, e = !1) {
  try {
    if (e && !Le(n))
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
function I(n, e) {
  return U(() => Te(n, e), [n, e]);
}
function Ne({
  value: n,
  onValueChange: e
}) {
  const [r, s] = G(n), o = O(e);
  o.current = e;
  const t = O(r);
  return t.current = r, P(() => {
    o.current(r);
  }, [r]), P(() => {
    re(n, t.current) || s(n);
  }, [n]), [r, s];
}
function X(n, e, r) {
  return n.filter(Boolean).map((s, o) => {
    var c;
    if (typeof s != "object")
      return e != null && e.fallback ? e.fallback(s) : s;
    const t = {
      ...s.props,
      key: ((c = s.props) == null ? void 0 : c.key) ?? (r ? `${r}-${o}` : `${o}`)
    };
    let l = t;
    Object.keys(s.slots).forEach((h) => {
      if (!s.slots[h] || !(s.slots[h] instanceof Element) && !s.slots[h].el)
        return;
      const a = h.split(".");
      a.forEach((m, g) => {
        l[m] || (l[m] = {}), g !== a.length - 1 && (l = t[m]);
      });
      const f = s.slots[h];
      let u, _, p = (e == null ? void 0 : e.clone) ?? !1;
      f instanceof Element ? u = f : (u = f.el, _ = f.callback, p = f.clone ?? !1), l[a[a.length - 1]] = u ? _ ? (...m) => (_(a[a.length - 1], m), /* @__PURE__ */ b.jsx(T, {
        slot: u,
        clone: p
      })) : /* @__PURE__ */ b.jsx(T, {
        slot: u,
        clone: p
      }) : l[a[a.length - 1]], l = t;
    });
    const i = (e == null ? void 0 : e.children) || "children";
    return s[i] && (t[i] = X(s[i], e, `${o}`)), t;
  });
}
const Me = Oe(({
  slots: n,
  children: e,
  onValueChange: r,
  filterOption: s,
  onChange: o,
  options: t,
  validateSearch: l,
  optionItems: i,
  getPopupContainer: c,
  elRef: h,
  ...a
}) => {
  const f = I(c), u = I(s), _ = I(l), [p, m] = Ne({
    onValueChange: r,
    value: a.value
  });
  return /* @__PURE__ */ b.jsxs(b.Fragment, {
    children: [/* @__PURE__ */ b.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ b.jsx(ne, {
      ...a,
      ref: h,
      value: p,
      options: U(() => t || X(i, {
        clone: !0
      }), [i, t]),
      onChange: (g, ...E) => {
        o == null || o(g, ...E), m(g);
      },
      validateSearch: _,
      notFoundContent: n.notFoundContent ? /* @__PURE__ */ b.jsx(T, {
        slot: n.notFoundContent
      }) : a.notFoundContent,
      filterOption: u || s,
      getPopupContainer: f
    })]
  });
});
export {
  Me as Mentions,
  Me as default
};
