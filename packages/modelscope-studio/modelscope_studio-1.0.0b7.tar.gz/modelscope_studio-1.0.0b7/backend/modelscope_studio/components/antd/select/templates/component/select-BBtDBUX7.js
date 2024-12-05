import { g as le, w as C } from "./Index-DJZqzkvx.js";
const E = window.ms_globals.React, te = window.ms_globals.React.forwardRef, ne = window.ms_globals.React.useRef, re = window.ms_globals.React.useState, oe = window.ms_globals.React.useEffect, q = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, se = window.ms_globals.antd.Select;
var B = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ce = E, ie = Symbol.for("react.element"), ae = Symbol.for("react.fragment"), ue = Object.prototype.hasOwnProperty, de = ce.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, fe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, t, r) {
  var o, l = {}, n = null, s = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) ue.call(t, o) && !fe.hasOwnProperty(o) && (l[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: ie,
    type: e,
    key: n,
    ref: s,
    props: l,
    _owner: de.current
  };
}
O.Fragment = ae;
O.jsx = V;
O.jsxs = V;
B.exports = O;
var g = B.exports;
const {
  SvelteComponent: _e,
  assign: A,
  binding_callbacks: W,
  check_outros: me,
  children: J,
  claim_element: Y,
  claim_space: he,
  component_subscribe: D,
  compute_slots: pe,
  create_slot: ge,
  detach: v,
  element: K,
  empty: M,
  exclude_internal_props: z,
  get_all_dirty_from_scope: we,
  get_slot_changes: be,
  group_outros: ye,
  init: Ee,
  insert_hydration: S,
  safe_not_equal: Re,
  set_custom_element_data: Q,
  space: Ie,
  transition_in: k,
  transition_out: T,
  update_slot_base: ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: Ce,
  onDestroy: Se,
  setContext: ke
} = window.__gradio__svelte__internal;
function G(e) {
  let t, r;
  const o = (
    /*#slots*/
    e[7].default
  ), l = ge(
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
      l && l.l(s), s.forEach(v), this.h();
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
        r ? be(
          o,
          /*$$scope*/
          n[6],
          s,
          null
        ) : we(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (k(l, n), r = !0);
    },
    o(n) {
      T(l, n), r = !1;
    },
    d(n) {
      n && v(t), l && l.d(n), e[9](null);
    }
  };
}
function Oe(e) {
  let t, r, o, l, n = (
    /*$$slots*/
    e[4].default && G(e)
  );
  return {
    c() {
      t = K("react-portal-target"), r = Ie(), n && n.c(), o = M(), this.h();
    },
    l(s) {
      t = Y(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(t).forEach(v), r = he(s), n && n.l(s), o = M(), this.h();
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
      16 && k(n, 1)) : (n = G(s), n.c(), k(n, 1), n.m(o.parentNode, o)) : n && (ye(), T(n, 1, 1, () => {
        n = null;
      }), me());
    },
    i(s) {
      l || (k(n), l = !0);
    },
    o(s) {
      T(n), l = !1;
    },
    d(s) {
      s && (v(t), v(r), v(o)), e[8](null), n && n.d(s);
    }
  };
}
function U(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Pe(e, t, r) {
  let o, l, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const i = pe(n);
  let {
    svelteInit: c
  } = t;
  const p = C(U(t)), u = C();
  D(e, u, (d) => r(0, o = d));
  const m = C();
  D(e, m, (d) => r(1, l = d));
  const a = [], h = Ce("$$ms-gr-react-wrapper"), {
    slotKey: f,
    slotIndex: _,
    subSlotIndex: w
  } = le() || {}, R = c({
    parent: h,
    props: p,
    target: u,
    slot: m,
    slotKey: f,
    slotIndex: _,
    subSlotIndex: w,
    onDestroy(d) {
      a.push(d);
    }
  });
  ke("$$ms-gr-react-wrapper", R), xe(() => {
    p.set(U(t));
  }), Se(() => {
    a.forEach((d) => d());
  });
  function I(d) {
    W[d ? "unshift" : "push"](() => {
      o = d, u.set(o);
    });
  }
  function P(d) {
    W[d ? "unshift" : "push"](() => {
      l = d, m.set(l);
    });
  }
  return e.$$set = (d) => {
    r(17, t = A(A({}, t), z(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, t = z(t), [o, l, u, m, i, c, s, n, I, P];
}
class je extends _e {
  constructor(t) {
    super(), Ee(this, t, Pe, Oe, Re, {
      svelteInit: 5
    });
  }
}
const H = window.ms_globals.rerender, j = window.ms_globals.tree;
function Fe(e) {
  function t(r) {
    const o = C(), l = new je({
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
            createPortal: F,
            node: j
          }), n.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== o), H({
              createPortal: F,
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
function Le(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const o = e[r];
    return typeof o == "number" && !Te.includes(r) ? t[r] = o + "px" : t[r] = o, t;
  }, {}) : {};
}
function L(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(F(E.cloneElement(e._reactElement, {
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
function Ne(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const b = te(({
  slot: e,
  clone: t,
  className: r,
  style: o
}, l) => {
  const n = ne(), [s, i] = re([]);
  return oe(() => {
    var m;
    if (!n.current || !e)
      return;
    let c = e;
    function p() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ne(l, a), r && a.classList.add(...r.split(" ")), o) {
        const h = Le(o);
        Object.keys(h).forEach((f) => {
          a.style[f] = h[f];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var w, R, I;
        (w = n.current) != null && w.contains(c) && ((R = n.current) == null || R.removeChild(c));
        const {
          portals: f,
          clonedElement: _
        } = L(e);
        return c = _, i(f), c.style.display = "contents", p(), (I = n.current) == null || I.appendChild(c), f.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", p(), (m = n.current) == null || m.appendChild(c);
    return () => {
      var a, h;
      c.style.display = "", (a = n.current) != null && a.contains(c) && ((h = n.current) == null || h.removeChild(c)), u == null || u.disconnect();
    };
  }, [e, t, r, o, l]), E.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ae(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function We(e, t = !1) {
  try {
    if (t && !Ae(e))
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
function y(e, t) {
  return q(() => We(e, t), [e, t]);
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
    Object.keys(o.slots).forEach((p) => {
      if (!o.slots[p] || !(o.slots[p] instanceof Element) && !o.slots[p].el)
        return;
      const u = p.split(".");
      u.forEach((_, w) => {
        s[_] || (s[_] = {}), w !== u.length - 1 && (s = n[_]);
      });
      const m = o.slots[p];
      let a, h, f = (t == null ? void 0 : t.clone) ?? !1;
      m instanceof Element ? a = m : (a = m.el, h = m.callback, f = m.clone ?? !1), s[u[u.length - 1]] = a ? h ? (..._) => (h(u[u.length - 1], _), /* @__PURE__ */ g.jsx(b, {
        slot: a,
        clone: f
      })) : /* @__PURE__ */ g.jsx(b, {
        slot: a,
        clone: f
      }) : s[u[u.length - 1]], s = n;
    });
    const i = (t == null ? void 0 : t.children) || "children";
    return o[i] && (n[i] = X(o[i], t, `${l}`)), n;
  });
}
function De(e, t) {
  return e ? /* @__PURE__ */ g.jsx(b, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function x({
  key: e,
  setSlotParams: t,
  slots: r
}, o) {
  return r[e] ? (...l) => (t(e, l), De(r[e], {
    clone: !0,
    ...o
  })) : void 0;
}
const ze = Fe(({
  slots: e,
  children: t,
  onValueChange: r,
  filterOption: o,
  onChange: l,
  options: n,
  optionItems: s,
  getPopupContainer: i,
  dropdownRender: c,
  optionRender: p,
  tagRender: u,
  labelRender: m,
  filterSort: a,
  elRef: h,
  setSlotParams: f,
  ..._
}) => {
  const w = y(i), R = y(o), I = y(c), P = y(a), d = y(p), Z = y(u), $ = y(m);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ g.jsx(se, {
      ..._,
      ref: h,
      options: q(() => n || X(s, {
        children: "options",
        clone: !0
      }), [s, n]),
      onChange: (N, ...ee) => {
        l == null || l(N, ...ee), r(N);
      },
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ g.jsx(b, {
          slot: e["allowClear.clearIcon"]
        })
      } : _.allowClear,
      removeIcon: e.removeIcon ? /* @__PURE__ */ g.jsx(b, {
        slot: e.removeIcon
      }) : _.removeIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ g.jsx(b, {
        slot: e.suffixIcon
      }) : _.suffixIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ g.jsx(b, {
        slot: e.notFoundContent
      }) : _.notFoundContent,
      menuItemSelectedIcon: e.menuItemSelectedIcon ? /* @__PURE__ */ g.jsx(b, {
        slot: e.menuItemSelectedIcon
      }) : _.menuItemSelectedIcon,
      filterOption: R || o,
      maxTagPlaceholder: e.maxTagPlaceholder ? x({
        slots: e,
        setSlotParams: f,
        key: "maxTagPlaceholder"
      }) : _.maxTagPlaceholder,
      getPopupContainer: w,
      dropdownRender: e.dropdownRender ? x({
        slots: e,
        setSlotParams: f,
        key: "dropdownRender"
      }) : I,
      optionRender: e.optionRender ? x({
        slots: e,
        setSlotParams: f,
        key: "optionRender"
      }) : d,
      tagRender: e.tagRender ? x({
        slots: e,
        setSlotParams: f,
        key: "tagRender"
      }) : Z,
      labelRender: e.labelRender ? x({
        slots: e,
        setSlotParams: f,
        key: "labelRender"
      }) : $,
      filterSort: P
    })]
  });
});
export {
  ze as Select,
  ze as default
};
