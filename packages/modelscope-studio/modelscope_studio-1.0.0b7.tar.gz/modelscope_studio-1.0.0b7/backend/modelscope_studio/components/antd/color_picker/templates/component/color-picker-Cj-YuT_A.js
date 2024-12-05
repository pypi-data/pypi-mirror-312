import { g as ne, w as R, d as re, a as v } from "./Index-sY9j5YrO.js";
const b = window.ms_globals.React, k = window.ms_globals.React.useMemo, q = window.ms_globals.React.useState, V = window.ms_globals.React.useEffect, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, j = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.ColorPicker;
var J = {
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
var se = b, le = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ce = Object.prototype.hasOwnProperty, ae = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Y(n, t, r) {
  var o, s = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (o in t) ce.call(t, o) && !ue.hasOwnProperty(o) && (s[o] = t[o]);
  if (n && n.defaultProps) for (o in t = n.defaultProps, t) s[o] === void 0 && (s[o] = t[o]);
  return {
    $$typeof: le,
    type: n,
    key: e,
    ref: l,
    props: s,
    _owner: ae.current
  };
}
O.Fragment = ie;
O.jsx = Y;
O.jsxs = Y;
J.exports = O;
var E = J.exports;
const {
  SvelteComponent: de,
  assign: F,
  binding_callbacks: N,
  check_outros: fe,
  children: K,
  claim_element: Q,
  claim_space: pe,
  component_subscribe: H,
  compute_slots: _e,
  create_slot: he,
  detach: S,
  element: X,
  empty: W,
  exclude_internal_props: D,
  get_all_dirty_from_scope: me,
  get_slot_changes: ge,
  group_outros: be,
  init: we,
  insert_hydration: I,
  safe_not_equal: ye,
  set_custom_element_data: Z,
  space: Ee,
  transition_in: C,
  transition_out: T,
  update_slot_base: xe
} = window.__gradio__svelte__internal, {
  beforeUpdate: Se,
  getContext: ve,
  onDestroy: Re,
  setContext: Ie
} = window.__gradio__svelte__internal;
function G(n) {
  let t, r;
  const o = (
    /*#slots*/
    n[7].default
  ), s = he(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = X("svelte-slot"), s && s.c(), this.h();
    },
    l(e) {
      t = Q(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = K(t);
      s && s.l(l), l.forEach(S), this.h();
    },
    h() {
      Z(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      I(e, t, l), s && s.m(t, null), n[9](t), r = !0;
    },
    p(e, l) {
      s && s.p && (!r || l & /*$$scope*/
      64) && xe(
        s,
        o,
        e,
        /*$$scope*/
        e[6],
        r ? ge(
          o,
          /*$$scope*/
          e[6],
          l,
          null
        ) : me(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (C(s, e), r = !0);
    },
    o(e) {
      T(s, e), r = !1;
    },
    d(e) {
      e && S(t), s && s.d(e), n[9](null);
    }
  };
}
function Ce(n) {
  let t, r, o, s, e = (
    /*$$slots*/
    n[4].default && G(n)
  );
  return {
    c() {
      t = X("react-portal-target"), r = Ee(), e && e.c(), o = W(), this.h();
    },
    l(l) {
      t = Q(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(t).forEach(S), r = pe(l), e && e.l(l), o = W(), this.h();
    },
    h() {
      Z(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      I(l, t, c), n[8](t), I(l, r, c), e && e.m(l, c), I(l, o, c), s = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = G(l), e.c(), C(e, 1), e.m(o.parentNode, o)) : e && (be(), T(e, 1, 1, () => {
        e = null;
      }), fe());
    },
    i(l) {
      s || (C(e), s = !0);
    },
    o(l) {
      T(e), s = !1;
    },
    d(l) {
      l && (S(t), S(r), S(o)), n[8](null), e && e.d(l);
    }
  };
}
function M(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function ke(n, t, r) {
  let o, s, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = _e(e);
  let {
    svelteInit: i
  } = t;
  const h = R(M(t)), a = R();
  H(n, a, (d) => r(0, o = d));
  const f = R();
  H(n, f, (d) => r(1, s = d));
  const u = [], m = ve("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: _,
    subSlotIndex: g
  } = ne() || {}, w = i({
    parent: m,
    props: h,
    target: a,
    slot: f,
    slotKey: p,
    slotIndex: _,
    subSlotIndex: g,
    onDestroy(d) {
      u.push(d);
    }
  });
  Ie("$$ms-gr-react-wrapper", w), Se(() => {
    h.set(M(t));
  }), Re(() => {
    u.forEach((d) => d());
  });
  function y(d) {
    N[d ? "unshift" : "push"](() => {
      o = d, a.set(o);
    });
  }
  function x(d) {
    N[d ? "unshift" : "push"](() => {
      s = d, f.set(s);
    });
  }
  return n.$$set = (d) => {
    r(17, t = F(F({}, t), D(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, l = d.$$scope);
  }, t = D(t), [o, s, a, f, c, i, l, e, y, x];
}
class Oe extends de {
  constructor(t) {
    super(), we(this, t, ke, Ce, ye, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, P = window.ms_globals.tree;
function Pe(n) {
  function t(r) {
    const o = R(), s = new Oe({
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
          }, c = e.parent ?? P;
          return c.nodes = [...c.nodes, l], z({
            createPortal: j,
            node: P
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), z({
              createPortal: j,
              node: P
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
function je(n) {
  const [t, r] = q(() => v(n));
  return V(() => {
    let o = !0;
    return n.subscribe((e) => {
      o && (o = !1, e === t) || r(e);
    });
  }, [n]), t;
}
function Te(n) {
  const t = k(() => re(n, (r) => r), [n]);
  return je(t);
}
function Le(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Ae(n, t = !1) {
  try {
    if (t && !Le(n))
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
function U(n, t) {
  return k(() => Ae(n, t), [n, t]);
}
function Fe(n, t) {
  const r = k(() => b.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, l) => {
    if (e.props.node.slotIndex && l.props.node.slotIndex) {
      const c = v(e.props.node.slotIndex) || 0, i = v(l.props.node.slotIndex) || 0;
      return c - i === 0 && e.props.node.subSlotIndex && l.props.node.subSlotIndex ? (v(e.props.node.subSlotIndex) || 0) - (v(l.props.node.subSlotIndex) || 0) : c - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Te(r);
}
const Ne = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function He(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const o = n[r];
    return typeof o == "number" && !Ne.includes(r) ? t[r] = o + "px" : t[r] = o, t;
  }, {}) : {};
}
function L(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(j(b.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: b.Children.toArray(n._reactElement.props.children).map((s) => {
        if (b.isValidElement(s) && s.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = L(s.props.el);
          return b.cloneElement(s, {
            ...s.props,
            el: l,
            children: [...b.Children.toArray(s.props.children), ...e]
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
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, l, i);
    });
  });
  const o = Array.from(n.childNodes);
  for (let s = 0; s < o.length; s++) {
    const e = o[s];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = L(e);
      t.push(...c), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function We(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const A = ee(({
  slot: n,
  clone: t,
  className: r,
  style: o
}, s) => {
  const e = te(), [l, c] = q([]);
  return V(() => {
    var f;
    if (!e.current || !n)
      return;
    let i = n;
    function h() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), We(s, u), r && u.classList.add(...r.split(" ")), o) {
        const m = He(o);
        Object.keys(m).forEach((p) => {
          u.style[p] = m[p];
        });
      }
    }
    let a = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var g, w, y;
        (g = e.current) != null && g.contains(i) && ((w = e.current) == null || w.removeChild(i));
        const {
          portals: p,
          clonedElement: _
        } = L(n);
        return i = _, c(p), i.style.display = "contents", h(), (y = e.current) == null || y.appendChild(i), p.length > 0;
      };
      u() || (a = new window.MutationObserver(() => {
        u() && (a == null || a.disconnect());
      }), a.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", h(), (f = e.current) == null || f.appendChild(i);
    return () => {
      var u, m;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((m = e.current) == null || m.removeChild(i)), a == null || a.disconnect();
    };
  }, [n, t, r, o, s]), b.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function $(n, t, r) {
  return n.filter(Boolean).map((o, s) => {
    var i;
    if (typeof o != "object")
      return o;
    const e = {
      ...o.props,
      key: ((i = o.props) == null ? void 0 : i.key) ?? (r ? `${r}-${s}` : `${s}`)
    };
    let l = e;
    Object.keys(o.slots).forEach((h) => {
      if (!o.slots[h] || !(o.slots[h] instanceof Element) && !o.slots[h].el)
        return;
      const a = h.split(".");
      a.forEach((_, g) => {
        l[_] || (l[_] = {}), g !== a.length - 1 && (l = e[_]);
      });
      const f = o.slots[h];
      let u, m, p = !1;
      f instanceof Element ? u = f : (u = f.el, m = f.callback, p = f.clone ?? !1), l[a[a.length - 1]] = u ? m ? (..._) => (m(a[a.length - 1], _), /* @__PURE__ */ E.jsx(A, {
        slot: u,
        clone: p
      })) : /* @__PURE__ */ E.jsx(A, {
        slot: u,
        clone: p
      }) : l[a[a.length - 1]], l = e;
    });
    const c = "children";
    return o[c] && (e[c] = $(o[c], t, `${s}`)), e;
  });
}
function De(n, t) {
  return n ? /* @__PURE__ */ E.jsx(A, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function B({
  key: n,
  setSlotParams: t,
  slots: r
}, o) {
  return r[n] ? (...s) => (t(n, s), De(r[n], {
    clone: !0,
    ...o
  })) : void 0;
}
const Me = Pe(({
  onValueChange: n,
  onChange: t,
  panelRender: r,
  showText: o,
  value: s,
  presets: e,
  presetItems: l,
  children: c,
  value_format: i,
  setSlotParams: h,
  slots: a,
  ...f
}) => {
  const u = U(r), m = U(o), p = Fe(c);
  return /* @__PURE__ */ E.jsxs(E.Fragment, {
    children: [p.length === 0 && /* @__PURE__ */ E.jsx("div", {
      style: {
        display: "none"
      },
      children: c
    }), /* @__PURE__ */ E.jsx(oe, {
      ...f,
      value: s,
      presets: k(() => e || $(l), [e, l]),
      showText: a.showText ? B({
        slots: a,
        setSlotParams: h,
        key: "showText"
      }) : m || o,
      panelRender: a.panelRender ? B({
        slots: a,
        setSlotParams: h,
        key: "panelRender"
      }) : u,
      onChange: (_, ...g) => {
        if (_.isGradient()) {
          const y = _.getColors().map((x) => {
            const d = {
              rgb: x.color.toRgbString(),
              hex: x.color.toHexString(),
              hsb: x.color.toHsbString()
            };
            return {
              ...x,
              color: d[i]
            };
          });
          t == null || t(y, ...g), n(y);
          return;
        }
        const w = {
          rgb: _.toRgbString(),
          hex: _.toHexString(),
          hsb: _.toHsbString()
        };
        t == null || t(w[i], ...g), n(w[i]);
      },
      children: p.length === 0 ? null : c
    })]
  });
});
export {
  Me as ColorPicker,
  Me as default
};
