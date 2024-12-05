import { g as oe, w as k } from "./Index-DiJg7R2a.js";
const E = window.ms_globals.React, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, ne = window.ms_globals.React.useState, re = window.ms_globals.React.useEffect, q = window.ms_globals.React.useMemo, T = window.ms_globals.ReactDOM.createPortal, le = window.ms_globals.antd.TreeSelect;
var B = {
  exports: {}
}, P = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var se = E, ce = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ae = Object.prototype.hasOwnProperty, ue = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, de = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, t, r) {
  var o, l = {}, n = null, s = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) ae.call(t, o) && !de.hasOwnProperty(o) && (l[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: ce,
    type: e,
    key: n,
    ref: s,
    props: l,
    _owner: ue.current
  };
}
P.Fragment = ie;
P.jsx = V;
P.jsxs = V;
B.exports = P;
var g = B.exports;
const {
  SvelteComponent: fe,
  assign: A,
  binding_callbacks: W,
  check_outros: _e,
  children: J,
  claim_element: Y,
  claim_space: he,
  component_subscribe: D,
  compute_slots: pe,
  create_slot: me,
  detach: R,
  element: K,
  empty: M,
  exclude_internal_props: U,
  get_all_dirty_from_scope: ge,
  get_slot_changes: we,
  group_outros: be,
  init: ye,
  insert_hydration: S,
  safe_not_equal: Ee,
  set_custom_element_data: Q,
  space: Re,
  transition_in: O,
  transition_out: F,
  update_slot_base: ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: Ce,
  onDestroy: Ie,
  setContext: ke
} = window.__gradio__svelte__internal;
function z(e) {
  let t, r;
  const o = (
    /*#slots*/
    e[7].default
  ), l = me(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      t = Y(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = J(t);
      l && l.l(s), s.forEach(R), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      S(n, t, s), l && l.m(t, null), e[9](t), r = !0;
    },
    p(n, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && ve(
        l,
        o,
        n,
        /*$$scope*/
        n[6],
        r ? we(
          o,
          /*$$scope*/
          n[6],
          s,
          null
        ) : ge(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (O(l, n), r = !0);
    },
    o(n) {
      F(l, n), r = !1;
    },
    d(n) {
      n && R(t), l && l.d(n), e[9](null);
    }
  };
}
function Se(e) {
  let t, r, o, l, n = (
    /*$$slots*/
    e[4].default && z(e)
  );
  return {
    c() {
      t = K("react-portal-target"), r = Re(), n && n.c(), o = M(), this.h();
    },
    l(s) {
      t = Y(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(t).forEach(R), r = he(s), n && n.l(s), o = M(), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      S(s, t, i), e[8](t), S(s, r, i), n && n.m(s, i), S(s, o, i), l = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, i), i & /*$$slots*/
      16 && O(n, 1)) : (n = z(s), n.c(), O(n, 1), n.m(o.parentNode, o)) : n && (be(), F(n, 1, 1, () => {
        n = null;
      }), _e());
    },
    i(s) {
      l || (O(n), l = !0);
    },
    o(s) {
      F(n), l = !1;
    },
    d(s) {
      s && (R(t), R(r), R(o)), e[8](null), n && n.d(s);
    }
  };
}
function G(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Oe(e, t, r) {
  let o, l, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const i = pe(n);
  let {
    svelteInit: c
  } = t;
  const m = k(G(t)), a = k();
  D(e, a, (d) => r(0, o = d));
  const _ = k();
  D(e, _, (d) => r(1, l = d));
  const u = [], f = Ce("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: h,
    subSlotIndex: w
  } = oe() || {}, b = c({
    parent: f,
    props: m,
    target: a,
    slot: _,
    slotKey: p,
    slotIndex: h,
    subSlotIndex: w,
    onDestroy(d) {
      u.push(d);
    }
  });
  ke("$$ms-gr-react-wrapper", b), xe(() => {
    m.set(G(t));
  }), Ie(() => {
    u.forEach((d) => d());
  });
  function y(d) {
    W[d ? "unshift" : "push"](() => {
      o = d, a.set(o);
    });
  }
  function I(d) {
    W[d ? "unshift" : "push"](() => {
      l = d, _.set(l);
    });
  }
  return e.$$set = (d) => {
    r(17, t = A(A({}, t), U(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, t = U(t), [o, l, a, _, i, c, s, n, y, I];
}
class Pe extends fe {
  constructor(t) {
    super(), ye(this, t, Oe, Se, Ee, {
      svelteInit: 5
    });
  }
}
const H = window.ms_globals.rerender, j = window.ms_globals.tree;
function je(e) {
  function t(r) {
    const o = k(), l = new Pe({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, i = n.parent ?? j;
          return i.nodes = [...i.nodes, s], H({
            createPortal: T,
            node: j
          }), n.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== o), H({
              createPortal: T,
              node: j
            });
          }), s;
        },
        ...r.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Te = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Fe(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const o = e[r];
    return typeof o == "number" && !Te.includes(r) ? t[r] = o + "px" : t[r] = o, t;
  }, {}) : {};
}
function L(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(T(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((l) => {
        if (E.isValidElement(l) && l.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = L(l.props.el);
          return E.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...E.Children.toArray(l.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((l) => {
    e.getEventListeners(l).forEach(({
      listener: s,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, s, c);
    });
  });
  const o = Array.from(e.childNodes);
  for (let l = 0; l < o.length; l++) {
    const n = o[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = L(n);
      t.push(...i), r.appendChild(s);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Le(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const v = ee(({
  slot: e,
  clone: t,
  className: r,
  style: o
}, l) => {
  const n = te(), [s, i] = ne([]);
  return re(() => {
    var _;
    if (!n.current || !e)
      return;
    let c = e;
    function m() {
      let u = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (u = c.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Le(l, u), r && u.classList.add(...r.split(" ")), o) {
        const f = Fe(o);
        Object.keys(f).forEach((p) => {
          u.style[p] = f[p];
        });
      }
    }
    let a = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var w, b, y;
        (w = n.current) != null && w.contains(c) && ((b = n.current) == null || b.removeChild(c));
        const {
          portals: p,
          clonedElement: h
        } = L(e);
        return c = h, i(p), c.style.display = "contents", m(), (y = n.current) == null || y.appendChild(c), p.length > 0;
      };
      u() || (a = new window.MutationObserver(() => {
        u() && (a == null || a.disconnect());
      }), a.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", m(), (_ = n.current) == null || _.appendChild(c);
    return () => {
      var u, f;
      c.style.display = "", (u = n.current) != null && u.contains(c) && ((f = n.current) == null || f.removeChild(c)), a == null || a.disconnect();
    };
  }, [e, t, r, o, l]), E.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ne(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Ae(e, t = !1) {
  try {
    if (t && !Ne(e))
      return;
    if (typeof e == "string") {
      let r = e.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function x(e, t) {
  return q(() => Ae(e, t), [e, t]);
}
function We(e) {
  return Object.keys(e).reduce((t, r) => (e[r] !== void 0 && (t[r] = e[r]), t), {});
}
function X(e, t, r) {
  return e.filter(Boolean).map((o, l) => {
    var c;
    if (typeof o != "object")
      return t != null && t.fallback ? t.fallback(o) : o;
    const n = {
      ...o.props,
      key: ((c = o.props) == null ? void 0 : c.key) ?? (r ? `${r}-${l}` : `${l}`)
    };
    let s = n;
    Object.keys(o.slots).forEach((m) => {
      if (!o.slots[m] || !(o.slots[m] instanceof Element) && !o.slots[m].el)
        return;
      const a = m.split(".");
      a.forEach((h, w) => {
        s[h] || (s[h] = {}), w !== a.length - 1 && (s = n[h]);
      });
      const _ = o.slots[m];
      let u, f, p = (t == null ? void 0 : t.clone) ?? !1;
      _ instanceof Element ? u = _ : (u = _.el, f = _.callback, p = _.clone ?? !1), s[a[a.length - 1]] = u ? f ? (...h) => (f(a[a.length - 1], h), /* @__PURE__ */ g.jsx(v, {
        slot: u,
        clone: p
      })) : /* @__PURE__ */ g.jsx(v, {
        slot: u,
        clone: p
      }) : s[a[a.length - 1]], s = n;
    });
    const i = (t == null ? void 0 : t.children) || "children";
    return o[i] && (n[i] = X(o[i], t, `${l}`)), n;
  });
}
function De(e, t) {
  return e ? /* @__PURE__ */ g.jsx(v, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function C({
  key: e,
  setSlotParams: t,
  slots: r
}, o) {
  return r[e] ? (...l) => (t(e, l), De(r[e], {
    clone: !0,
    ...o
  })) : void 0;
}
const Ue = je(({
  slots: e,
  filterTreeNode: t,
  getPopupContainer: r,
  dropdownRender: o,
  tagRender: l,
  treeTitleRender: n,
  treeData: s,
  onValueChange: i,
  onChange: c,
  children: m,
  slotItems: a,
  maxTagPlaceholder: _,
  elRef: u,
  setSlotParams: f,
  onLoadData: p,
  ...h
}) => {
  const w = x(t), b = x(r), y = x(l), I = x(o), d = x(n), Z = q(() => ({
    ...h,
    loadData: p,
    treeData: s || X(a, {
      clone: !0
    }),
    dropdownRender: e.dropdownRender ? C({
      slots: e,
      setSlotParams: f,
      key: "dropdownRender"
    }) : I,
    allowClear: e["allowClear.clearIcon"] ? {
      clearIcon: /* @__PURE__ */ g.jsx(v, {
        slot: e["allowClear.clearIcon"]
      })
    } : h.allowClear,
    suffixIcon: e.suffixIcon ? /* @__PURE__ */ g.jsx(v, {
      slot: e.suffixIcon
    }) : h.suffixIcon,
    switcherIcon: e.switcherIcon ? C({
      slots: e,
      setSlotParams: f,
      key: "switcherIcon"
    }) : h.switcherIcon,
    getPopupContainer: b,
    tagRender: e.tagRender ? C({
      slots: e,
      setSlotParams: f,
      key: "tagRender"
    }) : y,
    treeTitleRender: e.treeTitleRender ? C({
      slots: e,
      setSlotParams: f,
      key: "treeTitleRender"
    }) : d,
    filterTreeNode: w || t,
    maxTagPlaceholder: e.maxTagPlaceholder ? C({
      slots: e,
      setSlotParams: f,
      key: "maxTagPlaceholder"
    }) : _,
    notFoundContent: e.notFoundContent ? /* @__PURE__ */ g.jsx(v, {
      slot: e.notFoundContent
    }) : h.notFoundContent
  }), [I, t, w, b, _, p, h, f, a, e, y, s, d]);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: m
    }), /* @__PURE__ */ g.jsx(le, {
      ...We(Z),
      ref: u,
      onChange: (N, ...$) => {
        c == null || c(N, ...$), i(N);
      }
    })]
  });
});
export {
  Ue as TreeSelect,
  Ue as default
};
