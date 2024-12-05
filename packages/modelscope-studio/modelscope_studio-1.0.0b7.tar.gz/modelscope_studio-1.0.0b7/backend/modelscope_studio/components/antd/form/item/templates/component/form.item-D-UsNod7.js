import { g as le, w as I } from "./Index-uPmip_Cd.js";
const C = window.ms_globals.React, ne = window.ms_globals.React.forwardRef, oe = window.ms_globals.React.useRef, re = window.ms_globals.React.useState, se = window.ms_globals.React.useEffect, A = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, ie = window.ms_globals.internalContext.FormItemContext, ce = window.ms_globals.antd.Form;
var J = {
  exports: {}
}, j = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ae = C, ue = Symbol.for("react.element"), fe = Symbol.for("react.fragment"), de = Object.prototype.hasOwnProperty, pe = ae.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, _e = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Y(e, n, o) {
  var s, r = {}, t = null, l = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) de.call(n, s) && !_e.hasOwnProperty(s) && (r[s] = n[s]);
  if (e && e.defaultProps) for (s in n = e.defaultProps, n) r[s] === void 0 && (r[s] = n[s]);
  return {
    $$typeof: ue,
    type: e,
    key: t,
    ref: l,
    props: r,
    _owner: pe.current
  };
}
j.Fragment = fe;
j.jsx = Y;
j.jsxs = Y;
J.exports = j;
var h = J.exports;
const {
  SvelteComponent: me,
  assign: W,
  binding_callbacks: z,
  check_outros: he,
  children: K,
  claim_element: Q,
  claim_space: ge,
  component_subscribe: D,
  compute_slots: we,
  create_slot: be,
  detach: R,
  element: X,
  empty: V,
  exclude_internal_props: G,
  get_all_dirty_from_scope: ye,
  get_slot_changes: Ee,
  group_outros: xe,
  init: Ce,
  insert_hydration: F,
  safe_not_equal: ve,
  set_custom_element_data: Z,
  space: Re,
  transition_in: O,
  transition_out: L,
  update_slot_base: Ie
} = window.__gradio__svelte__internal, {
  beforeUpdate: Fe,
  getContext: Oe,
  onDestroy: Se,
  setContext: je
} = window.__gradio__svelte__internal;
function M(e) {
  let n, o;
  const s = (
    /*#slots*/
    e[7].default
  ), r = be(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = X("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      n = Q(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = K(n);
      r && r.l(l), l.forEach(R), this.h();
    },
    h() {
      Z(n, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      F(t, n, l), r && r.m(n, null), e[9](n), o = !0;
    },
    p(t, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && Ie(
        r,
        s,
        t,
        /*$$scope*/
        t[6],
        o ? Ee(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : ye(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (O(r, t), o = !0);
    },
    o(t) {
      L(r, t), o = !1;
    },
    d(t) {
      t && R(n), r && r.d(t), e[9](null);
    }
  };
}
function Pe(e) {
  let n, o, s, r, t = (
    /*$$slots*/
    e[4].default && M(e)
  );
  return {
    c() {
      n = X("react-portal-target"), o = Re(), t && t.c(), s = V(), this.h();
    },
    l(l) {
      n = Q(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(n).forEach(R), o = ge(l), t && t.l(l), s = V(), this.h();
    },
    h() {
      Z(n, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      F(l, n, c), e[8](n), F(l, o, c), t && t.m(l, c), F(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, c), c & /*$$slots*/
      16 && O(t, 1)) : (t = M(l), t.c(), O(t, 1), t.m(s.parentNode, s)) : t && (xe(), L(t, 1, 1, () => {
        t = null;
      }), he());
    },
    i(l) {
      r || (O(t), r = !0);
    },
    o(l) {
      L(t), r = !1;
    },
    d(l) {
      l && (R(n), R(o), R(s)), e[8](null), t && t.d(l);
    }
  };
}
function H(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function ke(e, n, o) {
  let s, r, {
    $$slots: t = {},
    $$scope: l
  } = n;
  const c = we(t);
  let {
    svelteInit: i
  } = n;
  const p = I(H(n)), a = I();
  D(e, a, (f) => o(0, s = f));
  const _ = I();
  D(e, _, (f) => o(1, r = f));
  const u = [], d = Oe("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: g,
    subSlotIndex: w
  } = le() || {}, v = i({
    parent: d,
    props: p,
    target: a,
    slot: _,
    slotKey: m,
    slotIndex: g,
    subSlotIndex: w,
    onDestroy(f) {
      u.push(f);
    }
  });
  je("$$ms-gr-react-wrapper", v), Fe(() => {
    p.set(H(n));
  }), Se(() => {
    u.forEach((f) => f());
  });
  function y(f) {
    z[f ? "unshift" : "push"](() => {
      s = f, a.set(s);
    });
  }
  function E(f) {
    z[f ? "unshift" : "push"](() => {
      r = f, _.set(r);
    });
  }
  return e.$$set = (f) => {
    o(17, n = W(W({}, n), G(f))), "svelteInit" in f && o(5, i = f.svelteInit), "$$scope" in f && o(6, l = f.$$scope);
  }, n = G(n), [s, r, a, _, c, i, l, t, y, E];
}
class Le extends me {
  constructor(n) {
    super(), Ce(this, n, ke, Pe, ve, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, P = window.ms_globals.tree;
function Te(e) {
  function n(o) {
    const s = I(), r = new Le({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? P;
          return c.nodes = [...c.nodes, l], U({
            createPortal: k,
            node: P
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), U({
              createPortal: k,
              node: P
            });
          }), l;
        },
        ...o.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Ae = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ne(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const s = e[o];
    return typeof s == "number" && !Ae.includes(o) ? n[o] = s + "px" : n[o] = s, n;
  }, {}) : {};
}
function T(e) {
  const n = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(k(C.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: C.Children.toArray(e._reactElement.props.children).map((r) => {
        if (C.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = T(r.props.el);
          return C.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...C.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(e.childNodes);
  for (let r = 0; r < s.length; r++) {
    const t = s[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = T(t);
      n.push(...c), o.appendChild(l);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function We(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const b = ne(({
  slot: e,
  clone: n,
  className: o,
  style: s
}, r) => {
  const t = oe(), [l, c] = re([]);
  return se(() => {
    var _;
    if (!t.current || !e)
      return;
    let i = e;
    function p() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), We(r, u), o && u.classList.add(...o.split(" ")), s) {
        const d = Ne(s);
        Object.keys(d).forEach((m) => {
          u.style[m] = d[m];
        });
      }
    }
    let a = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var w, v, y;
        (w = t.current) != null && w.contains(i) && ((v = t.current) == null || v.removeChild(i));
        const {
          portals: m,
          clonedElement: g
        } = T(e);
        return i = g, c(m), i.style.display = "contents", p(), (y = t.current) == null || y.appendChild(i), m.length > 0;
      };
      u() || (a = new window.MutationObserver(() => {
        u() && (a == null || a.disconnect());
      }), a.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", p(), (_ = t.current) == null || _.appendChild(i);
    return () => {
      var u, d;
      i.style.display = "", (u = t.current) != null && u.contains(i) && ((d = t.current) == null || d.removeChild(i)), a == null || a.disconnect();
    };
  }, [e, n, o, s, r]), C.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function ze(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function S(e, n = !1) {
  try {
    if (n && !ze(e))
      return;
    if (typeof e == "string") {
      let o = e.trim();
      return o.startsWith(";") && (o = o.slice(1)), o.endsWith(";") && (o = o.slice(0, -1)), new Function(`return (...args) => (${o})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function x(e, n) {
  return A(() => S(e, n), [e, n]);
}
function $(e, n, o) {
  return e.filter(Boolean).map((s, r) => {
    var i;
    if (typeof s != "object")
      return s;
    const t = {
      ...s.props,
      key: ((i = s.props) == null ? void 0 : i.key) ?? (o ? `${o}-${r}` : `${r}`)
    };
    let l = t;
    Object.keys(s.slots).forEach((p) => {
      if (!s.slots[p] || !(s.slots[p] instanceof Element) && !s.slots[p].el)
        return;
      const a = p.split(".");
      a.forEach((g, w) => {
        l[g] || (l[g] = {}), w !== a.length - 1 && (l = t[g]);
      });
      const _ = s.slots[p];
      let u, d, m = !1;
      _ instanceof Element ? u = _ : (u = _.el, d = _.callback, m = _.clone ?? !1), l[a[a.length - 1]] = u ? d ? (...g) => (d(a[a.length - 1], g), /* @__PURE__ */ h.jsx(b, {
        slot: u,
        clone: m
      })) : /* @__PURE__ */ h.jsx(b, {
        slot: u,
        clone: m
      }) : l[a[a.length - 1]], l = t;
    });
    const c = "children";
    return s[c] && (t[c] = $(s[c], n, `${r}`)), t;
  });
}
function De(e) {
  const n = e.pattern;
  return {
    ...e,
    pattern: (() => {
      if (typeof n == "string" && n.startsWith("/")) {
        const o = n.match(/^\/(.+)\/([gimuy]*)$/);
        if (o) {
          const [, s, r] = o;
          return new RegExp(s, r);
        }
      }
      return typeof n == "string" ? new RegExp(n) : void 0;
    })() ? new RegExp(n) : void 0,
    defaultField: S(e.defaultField) || e.defaultField,
    transform: S(e.transform),
    validator: S(e.validator)
  };
}
function q(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const B = ({
  children: e,
  ...n
}) => /* @__PURE__ */ h.jsx(ie.Provider, {
  value: A(() => n, [n]),
  children: e
}), Ge = Te(({
  slots: e,
  getValueFromEvent: n,
  getValueProps: o,
  normalize: s,
  shouldUpdate: r,
  tooltip: t,
  ruleItems: l,
  rules: c,
  children: i,
  hasFeedback: p,
  ...a
}) => {
  const _ = e["tooltip.icon"] || e["tooltip.title"] || typeof t == "object", u = typeof p == "object", d = q(p), m = x(d.icons), g = x(n), w = x(o), v = x(s), y = x(r), E = q(t), f = x(E.afterOpenChange), ee = x(E.getPopupContainer);
  return /* @__PURE__ */ h.jsx(ce.Item, {
    ...a,
    hasFeedback: u ? {
      ...d,
      icons: m || d.icons
    } : p,
    getValueFromEvent: g,
    getValueProps: w,
    normalize: v,
    shouldUpdate: y || r,
    rules: A(() => {
      var N;
      return (N = c || $(l)) == null ? void 0 : N.map((te) => De(te));
    }, [l, c]),
    tooltip: e.tooltip ? /* @__PURE__ */ h.jsx(b, {
      slot: e.tooltip
    }) : _ ? {
      ...E,
      afterOpenChange: f,
      getPopupContainer: ee,
      icon: e["tooltip.icon"] ? /* @__PURE__ */ h.jsx(b, {
        slot: e["tooltip.icon"]
      }) : E.icon,
      title: e["tooltip.title"] ? /* @__PURE__ */ h.jsx(b, {
        slot: e["tooltip.title"]
      }) : E.title
    } : t,
    extra: e.extra ? /* @__PURE__ */ h.jsx(b, {
      slot: e.extra
    }) : a.extra,
    help: e.help ? /* @__PURE__ */ h.jsx(b, {
      slot: e.help
    }) : a.help,
    label: e.label ? /* @__PURE__ */ h.jsx(b, {
      slot: e.label
    }) : a.label,
    children: y || r ? () => /* @__PURE__ */ h.jsx(B, {
      children: i
    }) : /* @__PURE__ */ h.jsx(B, {
      children: i
    })
  });
});
export {
  Ge as FormItem,
  Ge as default
};
