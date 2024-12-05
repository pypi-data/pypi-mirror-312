import { g as ee, w as C, d as te, a as y } from "./Index-BNLfueUt.js";
const _ = window.ms_globals.React, F = window.ms_globals.React.useMemo, U = window.ms_globals.React.useState, H = window.ms_globals.React.useEffect, Z = window.ms_globals.React.forwardRef, $ = window.ms_globals.React.useRef, k = window.ms_globals.ReactDOM.createPortal, T = window.ms_globals.antd.Card;
var K = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = _, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(n, t, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) se.call(t, s) && !ae.hasOwnProperty(s) && (o[s] = t[s]);
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
R.Fragment = oe;
R.jsx = V;
R.jsxs = V;
K.exports = R;
var h = K.exports;
const {
  SvelteComponent: ie,
  assign: A,
  binding_callbacks: N,
  check_outros: ce,
  children: q,
  claim_element: J,
  claim_space: de,
  component_subscribe: B,
  compute_slots: ue,
  create_slot: fe,
  detach: g,
  element: Y,
  empty: D,
  exclude_internal_props: G,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: I,
  safe_not_equal: ge,
  set_custom_element_data: Q,
  space: be,
  transition_in: S,
  transition_out: j,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: xe,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function M(n) {
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
      t = Y("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = J(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = q(t);
      o && o.l(l), l.forEach(g), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      I(e, t, l), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && we(
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
      j(o, e), r = !1;
    },
    d(e) {
      e && g(t), o && o.d(e), n[9](null);
    }
  };
}
function Ce(n) {
  let t, r, s, o, e = (
    /*$$slots*/
    n[4].default && M(n)
  );
  return {
    c() {
      t = Y("react-portal-target"), r = be(), e && e.c(), s = D(), this.h();
    },
    l(l) {
      t = J(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(t).forEach(g), r = de(l), e && e.l(l), s = D(), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      I(l, t, i), n[8](t), I(l, r, i), e && e.m(l, i), I(l, s, i), o = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, i), i & /*$$slots*/
      16 && S(e, 1)) : (e = M(l), e.c(), S(e, 1), e.m(s.parentNode, s)) : e && (me(), j(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(l) {
      o || (S(e), o = !0);
    },
    o(l) {
      j(e), o = !1;
    },
    d(l) {
      l && (g(t), g(r), g(s)), n[8](null), e && e.d(l);
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
function Ie(n, t, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const i = ue(e);
  let {
    svelteInit: a
  } = t;
  const b = C(W(t)), u = C();
  B(n, u, (c) => r(0, s = c));
  const m = C();
  B(n, m, (c) => r(1, o = c));
  const d = [], f = xe("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: O,
    subSlotIndex: x
  } = ee() || {}, E = a({
    parent: f,
    props: b,
    target: u,
    slot: m,
    slotKey: p,
    slotIndex: O,
    subSlotIndex: x,
    onDestroy(c) {
      d.push(c);
    }
  });
  ve("$$ms-gr-react-wrapper", E), ye(() => {
    b.set(W(t));
  }), Ee(() => {
    d.forEach((c) => c());
  });
  function v(c) {
    N[c ? "unshift" : "push"](() => {
      s = c, u.set(s);
    });
  }
  function X(c) {
    N[c ? "unshift" : "push"](() => {
      o = c, m.set(o);
    });
  }
  return n.$$set = (c) => {
    r(17, t = A(A({}, t), G(c))), "svelteInit" in c && r(5, a = c.svelteInit), "$$scope" in c && r(6, l = c.$$scope);
  }, t = G(t), [s, o, u, m, i, a, l, e, v, X];
}
class Se extends ie {
  constructor(t) {
    super(), he(this, t, Ie, Ce, ge, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, P = window.ms_globals.tree;
function Re(n) {
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
          }, i = e.parent ?? P;
          return i.nodes = [...i.nodes, l], z({
            createPortal: k,
            node: P
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((a) => a.svelteInstance !== s), z({
              createPortal: k,
              node: P
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
function Oe(n) {
  const [t, r] = U(() => y(n));
  return H(() => {
    let s = !0;
    return n.subscribe((e) => {
      s && (s = !1, e === t) || r(e);
    });
  }, [n]), t;
}
function Pe(n) {
  const t = F(() => te(n, (r) => r), [n]);
  return Oe(t);
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const s = n[r];
    return typeof s == "number" && !ke.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function L(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(k(_.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: _.Children.toArray(n._reactElement.props.children).map((o) => {
        if (_.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = L(o.props.el);
          return _.cloneElement(o, {
            ...o.props,
            el: l,
            children: [..._.Children.toArray(o.props.children), ...e]
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
      type: i,
      useCapture: a
    }) => {
      r.addEventListener(i, l, a);
    });
  });
  const s = Array.from(n.childNodes);
  for (let o = 0; o < s.length; o++) {
    const e = s[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = L(e);
      t.push(...i), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Le(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const w = Z(({
  slot: n,
  clone: t,
  className: r,
  style: s
}, o) => {
  const e = $(), [l, i] = U([]);
  return H(() => {
    var m;
    if (!e.current || !n)
      return;
    let a = n;
    function b() {
      let d = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (d = a.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Le(o, d), r && d.classList.add(...r.split(" ")), s) {
        const f = je(s);
        Object.keys(f).forEach((p) => {
          d.style[p] = f[p];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var x, E, v;
        (x = e.current) != null && x.contains(a) && ((E = e.current) == null || E.removeChild(a));
        const {
          portals: p,
          clonedElement: O
        } = L(n);
        return a = O, i(p), a.style.display = "contents", b(), (v = e.current) == null || v.appendChild(a), p.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      a.style.display = "contents", b(), (m = e.current) == null || m.appendChild(a);
    return () => {
      var d, f;
      a.style.display = "", (d = e.current) != null && d.contains(a) && ((f = e.current) == null || f.removeChild(a)), u == null || u.disconnect();
    };
  }, [n, t, r, s, o]), _.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Te(n, t) {
  const r = F(() => _.Children.toArray(n).filter((e) => e.props.node && t === e.props.nodeSlotKey).sort((e, l) => {
    if (e.props.node.slotIndex && l.props.node.slotIndex) {
      const i = y(e.props.node.slotIndex) || 0, a = y(l.props.node.slotIndex) || 0;
      return i - a === 0 && e.props.node.subSlotIndex && l.props.node.subSlotIndex ? (y(e.props.node.subSlotIndex) || 0) - (y(l.props.node.subSlotIndex) || 0) : i - a;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Pe(r);
}
const Ne = Re(({
  children: n,
  containsGrid: t,
  slots: r,
  ...s
}) => {
  const o = Te(n, "actions");
  return /* @__PURE__ */ h.jsxs(T, {
    ...s,
    title: r.title ? /* @__PURE__ */ h.jsx(w, {
      slot: r.title
    }) : s.title,
    extra: r.extra ? /* @__PURE__ */ h.jsx(w, {
      slot: r.extra
    }) : s.extra,
    cover: r.cover ? /* @__PURE__ */ h.jsx(w, {
      slot: r.cover
    }) : s.cover,
    tabBarExtraContent: r.tabBarExtraContent ? /* @__PURE__ */ h.jsx(w, {
      slot: r.tabBarExtraContent
    }) : s.tabBarExtraContent,
    actions: o.length > 0 ? o.map((e, l) => /* @__PURE__ */ h.jsx(w, {
      slot: e
    }, l)) : s.actions,
    children: [t ? /* @__PURE__ */ h.jsx(T.Grid, {
      style: {
        display: "none"
      }
    }) : null, n]
  });
});
export {
  Ne as Card,
  Ne as default
};
