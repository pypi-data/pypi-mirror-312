import { g as ee, w as R } from "./Index-D0lue7OT.js";
const w = window.ms_globals.React, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, G = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Tour;
var U = {
  exports: {}
}, C = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = w, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(n, t, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) se.call(t, s) && !ce.hasOwnProperty(s) && (o[s] = t[s]);
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
C.Fragment = oe;
C.jsx = H;
C.jsxs = H;
U.exports = C;
var g = U.exports;
const {
  SvelteComponent: ie,
  assign: T,
  binding_callbacks: L,
  check_outros: ae,
  children: q,
  claim_element: B,
  claim_space: ue,
  component_subscribe: F,
  compute_slots: de,
  create_slot: fe,
  detach: y,
  element: V,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: he,
  init: me,
  insert_hydration: x,
  safe_not_equal: ge,
  set_custom_element_data: J,
  space: we,
  transition_in: S,
  transition_out: k,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: Ee,
  onDestroy: ve,
  setContext: Re
} = window.__gradio__svelte__internal;
function W(n) {
  let t, r;
  const s = (
    /*#slots*/
    n[7].default
  ), o = fe(
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
      o && o.l(l), l.forEach(y), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      x(e, t, l), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && be(
        o,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? _e(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (S(o, e), r = !0);
    },
    o(e) {
      k(o, e), r = !1;
    },
    d(e) {
      e && y(t), o && o.d(e), n[9](null);
    }
  };
}
function xe(n) {
  let t, r, s, o, e = (
    /*$$slots*/
    n[4].default && W(n)
  );
  return {
    c() {
      t = V("react-portal-target"), r = we(), e && e.c(), s = N(), this.h();
    },
    l(l) {
      t = B(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(t).forEach(y), r = ue(l), e && e.l(l), s = N(), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      x(l, t, a), n[8](t), x(l, r, a), e && e.m(l, a), x(l, s, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, a), a & /*$$slots*/
      16 && S(e, 1)) : (e = W(l), e.c(), S(e, 1), e.m(s.parentNode, s)) : e && (he(), k(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(l) {
      o || (S(e), o = !0);
    },
    o(l) {
      k(e), o = !1;
    },
    d(l) {
      l && (y(t), y(r), y(s)), n[8](null), e && e.d(l);
    }
  };
}
function D(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Se(n, t, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const a = de(e);
  let {
    svelteInit: c
  } = t;
  const p = R(D(t)), u = R();
  F(n, u, (d) => r(0, s = d));
  const f = R();
  F(n, f, (d) => r(1, o = d));
  const i = [], _ = Ee("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: m,
    subSlotIndex: b
  } = ee() || {}, E = c({
    parent: _,
    props: p,
    target: u,
    slot: f,
    slotKey: h,
    slotIndex: m,
    subSlotIndex: b,
    onDestroy(d) {
      i.push(d);
    }
  });
  Re("$$ms-gr-react-wrapper", E), ye(() => {
    p.set(D(t));
  }), ve(() => {
    i.forEach((d) => d());
  });
  function v(d) {
    L[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function K(d) {
    L[d ? "unshift" : "push"](() => {
      o = d, f.set(o);
    });
  }
  return n.$$set = (d) => {
    r(17, t = T(T({}, t), A(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, l = d.$$scope);
  }, t = A(t), [s, o, u, f, a, c, l, e, v, K];
}
class Ie extends ie {
  constructor(t) {
    super(), me(this, t, Se, xe, ge, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ce(n) {
  function t(r) {
    const s = R(), o = new Ie({
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
          }, a = e.parent ?? O;
          return a.nodes = [...a.nodes, l], M({
            createPortal: P,
            node: O
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== s), M({
              createPortal: P,
              node: O
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
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const s = n[r];
    return typeof s == "number" && !Oe.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function j(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((o) => {
        if (w.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = j(o.props.el);
          return w.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...w.Children.toArray(o.props.children), ...e]
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
      type: a,
      useCapture: c
    }) => {
      r.addEventListener(a, l, c);
    });
  });
  const s = Array.from(n.childNodes);
  for (let o = 0; o < s.length; o++) {
    const e = s[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = j(e);
      t.push(...a), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function ke(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const I = Q(({
  slot: n,
  clone: t,
  className: r,
  style: s
}, o) => {
  const e = X(), [l, a] = Z([]);
  return $(() => {
    var f;
    if (!e.current || !n)
      return;
    let c = n;
    function p() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), ke(o, i), r && i.classList.add(...r.split(" ")), s) {
        const _ = Pe(s);
        Object.keys(_).forEach((h) => {
          i.style[h] = _[h];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var b, E, v;
        (b = e.current) != null && b.contains(c) && ((E = e.current) == null || E.removeChild(c));
        const {
          portals: h,
          clonedElement: m
        } = j(n);
        return c = m, a(h), c.style.display = "contents", p(), (v = e.current) == null || v.appendChild(c), h.length > 0;
      };
      i() || (u = new window.MutationObserver(() => {
        i() && (u == null || u.disconnect());
      }), u.observe(n, {
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
  }, [n, t, r, s, o]), w.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function je(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Te(n, t = !1) {
  try {
    if (t && !je(n))
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
function z(n, t) {
  return G(() => Te(n, t), [n, t]);
}
function Y(n, t, r) {
  return n.filter(Boolean).map((s, o) => {
    var c;
    if (typeof s != "object")
      return s;
    const e = {
      ...s.props,
      key: ((c = s.props) == null ? void 0 : c.key) ?? (r ? `${r}-${o}` : `${o}`)
    };
    let l = e;
    Object.keys(s.slots).forEach((p) => {
      if (!s.slots[p] || !(s.slots[p] instanceof Element) && !s.slots[p].el)
        return;
      const u = p.split(".");
      u.forEach((m, b) => {
        l[m] || (l[m] = {}), b !== u.length - 1 && (l = e[m]);
      });
      const f = s.slots[p];
      let i, _, h = !1;
      f instanceof Element ? i = f : (i = f.el, _ = f.callback, h = f.clone ?? !1), l[u[u.length - 1]] = i ? _ ? (...m) => (_(u[u.length - 1], m), /* @__PURE__ */ g.jsx(I, {
        slot: i,
        clone: h
      })) : /* @__PURE__ */ g.jsx(I, {
        slot: i,
        clone: h
      }) : l[u[u.length - 1]], l = e;
    });
    const a = "children";
    return s[a] && (e[a] = Y(s[a], t, `${o}`)), e;
  });
}
function Le(n, t) {
  return n ? /* @__PURE__ */ g.jsx(I, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Fe({
  key: n,
  setSlotParams: t,
  slots: r
}, s) {
  return r[n] ? (...o) => (t(n, o), Le(r[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ae = Ce(({
  slots: n,
  steps: t,
  slotItems: r,
  children: s,
  onChange: o,
  onClose: e,
  getPopupContainer: l,
  setSlotParams: a,
  indicatorsRender: c,
  ...p
}) => {
  const u = z(l), f = z(c);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: s
    }), /* @__PURE__ */ g.jsx(te, {
      ...p,
      steps: G(() => t || Y(r), [t, r]),
      onChange: (i) => {
        o == null || o(i);
      },
      closeIcon: n.closeIcon ? /* @__PURE__ */ g.jsx(I, {
        slot: n.closeIcon
      }) : p.closeIcon,
      indicatorsRender: n.indicatorsRender ? Fe({
        slots: n,
        setSlotParams: a,
        key: "indicatorsRender"
      }) : f,
      getPopupContainer: u,
      onClose: (i, ..._) => {
        e == null || e(i, ..._);
      }
    })]
  });
});
export {
  Ae as Tour,
  Ae as default
};
