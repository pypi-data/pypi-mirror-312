import { g as te, w as x } from "./Index-C_NhDObK.js";
const g = window.ms_globals.React, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, $ = window.ms_globals.React.useState, ee = window.ms_globals.React.useEffect, U = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.antd.Dropdown;
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
var re = g, oe = Symbol.for("react.element"), le = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, ce = re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function q(n, e, o) {
  var r, l = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (r in e) se.call(e, r) && !ie.hasOwnProperty(r) && (l[r] = e[r]);
  if (n && n.defaultProps) for (r in e = n.defaultProps, e) l[r] === void 0 && (l[r] = e[r]);
  return {
    $$typeof: oe,
    type: n,
    key: t,
    ref: s,
    props: l,
    _owner: ce.current
  };
}
S.Fragment = le;
S.jsx = q;
S.jsxs = q;
H.exports = S;
var w = H.exports;
const {
  SvelteComponent: ae,
  assign: L,
  binding_callbacks: F,
  check_outros: ue,
  children: B,
  claim_element: V,
  claim_space: de,
  component_subscribe: N,
  compute_slots: fe,
  create_slot: _e,
  detach: y,
  element: J,
  empty: T,
  exclude_internal_props: A,
  get_all_dirty_from_scope: me,
  get_slot_changes: pe,
  group_outros: he,
  init: we,
  insert_hydration: R,
  safe_not_equal: ge,
  set_custom_element_data: Y,
  space: be,
  transition_in: C,
  transition_out: P,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ve,
  onDestroy: xe,
  setContext: Re
} = window.__gradio__svelte__internal;
function D(n) {
  let e, o;
  const r = (
    /*#slots*/
    n[7].default
  ), l = _e(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = J("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      e = V(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = B(e);
      l && l.l(s), s.forEach(y), this.h();
    },
    h() {
      Y(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      R(t, e, s), l && l.m(e, null), n[9](e), o = !0;
    },
    p(t, s) {
      l && l.p && (!o || s & /*$$scope*/
      64) && ye(
        l,
        r,
        t,
        /*$$scope*/
        t[6],
        o ? pe(
          r,
          /*$$scope*/
          t[6],
          s,
          null
        ) : me(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (C(l, t), o = !0);
    },
    o(t) {
      P(l, t), o = !1;
    },
    d(t) {
      t && y(e), l && l.d(t), n[9](null);
    }
  };
}
function Ce(n) {
  let e, o, r, l, t = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      e = J("react-portal-target"), o = be(), t && t.c(), r = T(), this.h();
    },
    l(s) {
      e = V(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), B(e).forEach(y), o = de(s), t && t.l(s), r = T(), this.h();
    },
    h() {
      Y(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      R(s, e, c), n[8](e), R(s, o, c), t && t.m(s, c), R(s, r, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && C(t, 1)) : (t = D(s), t.c(), C(t, 1), t.m(r.parentNode, r)) : t && (he(), P(t, 1, 1, () => {
        t = null;
      }), ue());
    },
    i(s) {
      l || (C(t), l = !0);
    },
    o(s) {
      P(t), l = !1;
    },
    d(s) {
      s && (y(e), y(o), y(r)), n[8](null), t && t.d(s);
    }
  };
}
function W(n) {
  const {
    svelteInit: e,
    ...o
  } = n;
  return o;
}
function Ie(n, e, o) {
  let r, l, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const c = fe(t);
  let {
    svelteInit: i
  } = e;
  const m = x(W(e)), u = x();
  N(n, u, (d) => o(0, r = d));
  const f = x();
  N(n, f, (d) => o(1, l = d));
  const a = [], _ = ve("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: h,
    subSlotIndex: b
  } = te() || {}, E = i({
    parent: _,
    props: m,
    target: u,
    slot: f,
    slotKey: p,
    slotIndex: h,
    subSlotIndex: b,
    onDestroy(d) {
      a.push(d);
    }
  });
  Re("$$ms-gr-react-wrapper", E), Ee(() => {
    m.set(W(e));
  }), xe(() => {
    a.forEach((d) => d());
  });
  function v(d) {
    F[d ? "unshift" : "push"](() => {
      r = d, u.set(r);
    });
  }
  function Q(d) {
    F[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  return n.$$set = (d) => {
    o(17, e = L(L({}, e), A(d))), "svelteInit" in d && o(5, i = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, e = A(e), [r, l, u, f, c, i, s, t, v, Q];
}
class Se extends ae {
  constructor(e) {
    super(), we(this, e, Ie, Ce, ge, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, k = window.ms_globals.tree;
function ke(n) {
  function e(o) {
    const r = x(), l = new Se({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? k;
          return c.nodes = [...c.nodes, s], M({
            createPortal: O,
            node: k
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== r), M({
              createPortal: O,
              node: k
            });
          }), s;
        },
        ...o.props
      }
    });
    return r.set(l), l;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(e);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((e, o) => {
    const r = n[o];
    return typeof r == "number" && !Oe.includes(o) ? e[o] = r + "px" : e[o] = r, e;
  }, {}) : {};
}
function j(n) {
  const e = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(O(g.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: g.Children.toArray(n._reactElement.props.children).map((l) => {
        if (g.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = j(l.props.el);
          return g.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...g.Children.toArray(l.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((l) => {
    n.getEventListeners(l).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, s, i);
    });
  });
  const r = Array.from(n.childNodes);
  for (let l = 0; l < r.length; l++) {
    const t = r[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = j(t);
      e.push(...c), o.appendChild(s);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function je(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const I = X(({
  slot: n,
  clone: e,
  className: o,
  style: r
}, l) => {
  const t = Z(), [s, c] = $([]);
  return ee(() => {
    var f;
    if (!t.current || !n)
      return;
    let i = n;
    function m() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), je(l, a), o && a.classList.add(...o.split(" ")), r) {
        const _ = Pe(r);
        Object.keys(_).forEach((p) => {
          a.style[p] = _[p];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var b, E, v;
        (b = t.current) != null && b.contains(i) && ((E = t.current) == null || E.removeChild(i));
        const {
          portals: p,
          clonedElement: h
        } = j(n);
        return i = h, c(p), i.style.display = "contents", m(), (v = t.current) == null || v.appendChild(i), p.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", m(), (f = t.current) == null || f.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((_ = t.current) == null || _.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, e, o, r, l]), g.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Fe(n, e = !1) {
  try {
    if (e && !Le(n))
      return;
    if (typeof n == "string") {
      let o = n.trim();
      return o.startsWith(";") && (o = o.slice(1)), o.endsWith(";") && (o = o.slice(0, -1)), new Function(`return (...args) => (${o})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function z(n, e) {
  return U(() => Fe(n, e), [n, e]);
}
function K(n, e, o) {
  return n.filter(Boolean).map((r, l) => {
    var i;
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const t = {
      ...r.props,
      key: ((i = r.props) == null ? void 0 : i.key) ?? (o ? `${o}-${l}` : `${l}`)
    };
    let s = t;
    Object.keys(r.slots).forEach((m) => {
      if (!r.slots[m] || !(r.slots[m] instanceof Element) && !r.slots[m].el)
        return;
      const u = m.split(".");
      u.forEach((h, b) => {
        s[h] || (s[h] = {}), b !== u.length - 1 && (s = t[h]);
      });
      const f = r.slots[m];
      let a, _, p = (e == null ? void 0 : e.clone) ?? !1;
      f instanceof Element ? a = f : (a = f.el, _ = f.callback, p = f.clone ?? !1), s[u[u.length - 1]] = a ? _ ? (...h) => (_(u[u.length - 1], h), /* @__PURE__ */ w.jsx(I, {
        slot: a,
        clone: p
      })) : /* @__PURE__ */ w.jsx(I, {
        slot: a,
        clone: p
      }) : s[u[u.length - 1]], s = t;
    });
    const c = (e == null ? void 0 : e.children) || "children";
    return r[c] && (t[c] = K(r[c], e, `${l}`)), t;
  });
}
function Ne(n, e) {
  return n ? /* @__PURE__ */ w.jsx(I, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function G({
  key: n,
  setSlotParams: e,
  slots: o
}, r) {
  return o[n] ? (...l) => (e(n, l), Ne(o[n], {
    clone: !0,
    ...r
  })) : void 0;
}
const Ae = ke(({
  getPopupContainer: n,
  innerStyle: e,
  children: o,
  slots: r,
  menuItems: l,
  dropdownRender: t,
  setSlotParams: s,
  ...c
}) => {
  var u, f, a;
  const i = z(n), m = z(t);
  return /* @__PURE__ */ w.jsx(w.Fragment, {
    children: /* @__PURE__ */ w.jsx(ne, {
      ...c,
      menu: {
        ...c.menu,
        items: U(() => {
          var _;
          return ((_ = c.menu) == null ? void 0 : _.items) || K(l, {
            clone: !0
          });
        }, [l, (u = c.menu) == null ? void 0 : u.items]),
        expandIcon: r["menu.expandIcon"] ? G({
          slots: r,
          setSlotParams: s,
          key: "menu.expandIcon"
        }, {
          clone: !0
        }) : (f = c.menu) == null ? void 0 : f.expandIcon,
        overflowedIndicator: r["menu.overflowedIndicator"] ? /* @__PURE__ */ w.jsx(I, {
          slot: r["menu.overflowedIndicator"]
        }) : (a = c.menu) == null ? void 0 : a.overflowedIndicator
      },
      getPopupContainer: i,
      dropdownRender: r.dropdownRender ? G({
        slots: r,
        setSlotParams: s,
        key: "dropdownRender"
      }, {
        clone: !0
      }) : m,
      children: /* @__PURE__ */ w.jsx("div", {
        className: "ms-gr-antd-dropdown-content",
        style: {
          display: "inline-block",
          ...e
        },
        children: o
      })
    })
  });
});
export {
  Ae as Dropdown,
  Ae as default
};
