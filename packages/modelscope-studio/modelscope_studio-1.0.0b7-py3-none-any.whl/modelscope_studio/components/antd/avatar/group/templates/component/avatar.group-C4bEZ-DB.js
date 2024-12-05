import { g as $, w as E, d as ee, a as w } from "./Index-76I8Vxox.js";
const h = window.ms_globals.React, z = window.ms_globals.React.useMemo, U = window.ms_globals.React.useState, H = window.ms_globals.React.useEffect, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, k = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Avatar;
var K = {
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
var ne = h, oe = Symbol.for("react.element"), re = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) se.call(t, l) && !ae.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: oe,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: le.current
  };
}
C.Fragment = re;
C.jsx = V;
C.jsxs = V;
K.exports = C;
var g = K.exports;
const {
  SvelteComponent: ie,
  assign: L,
  binding_callbacks: T,
  check_outros: ce,
  children: q,
  claim_element: B,
  claim_space: de,
  component_subscribe: N,
  compute_slots: ue,
  create_slot: pe,
  detach: v,
  element: J,
  empty: D,
  exclude_internal_props: G,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: I,
  safe_not_equal: ge,
  set_custom_element_data: Y,
  space: ve,
  transition_in: S,
  transition_out: A,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: be,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function F(n) {
  let t, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = pe(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = J("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = B(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = q(t);
      r && r.l(s), s.forEach(v), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      I(e, t, s), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && we(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? _e(
          l,
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
      o || (S(r, e), o = !0);
    },
    o(e) {
      A(r, e), o = !1;
    },
    d(e) {
      e && v(t), r && r.d(e), n[9](null);
    }
  };
}
function Ie(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = J("react-portal-target"), o = ve(), e && e.c(), l = D(), this.h();
    },
    l(s) {
      t = B(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(t).forEach(v), o = de(s), e && e.l(s), l = D(), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      I(s, t, i), n[8](t), I(s, o, i), e && e.m(s, i), I(s, l, i), r = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && S(e, 1)) : (e = F(s), e.c(), S(e, 1), e.m(l.parentNode, l)) : e && (me(), A(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      r || (S(e), r = !0);
    },
    o(s) {
      A(e), r = !1;
    },
    d(s) {
      s && (v(t), v(o), v(l)), n[8](null), e && e.d(s);
    }
  };
}
function M(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Se(n, t, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = ue(e);
  let {
    svelteInit: a
  } = t;
  const f = E(M(t)), u = E();
  N(n, u, (c) => o(0, l = c));
  const p = E();
  N(n, p, (c) => o(1, r = c));
  const d = [], _ = be("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: R,
    subSlotIndex: x
  } = $() || {}, b = a({
    parent: _,
    props: f,
    target: u,
    slot: p,
    slotKey: m,
    slotIndex: R,
    subSlotIndex: x,
    onDestroy(c) {
      d.push(c);
    }
  });
  Ee("$$ms-gr-react-wrapper", b), xe(() => {
    f.set(M(t));
  }), ye(() => {
    d.forEach((c) => c());
  });
  function y(c) {
    T[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  function Q(c) {
    T[c ? "unshift" : "push"](() => {
      r = c, p.set(r);
    });
  }
  return n.$$set = (c) => {
    o(17, t = L(L({}, t), G(c))), "svelteInit" in c && o(5, a = c.svelteInit), "$$scope" in c && o(6, s = c.$$scope);
  }, t = G(t), [l, r, u, p, i, a, s, e, y, Q];
}
class Ce extends ie {
  constructor(t) {
    super(), he(this, t, Se, Ie, ge, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, O = window.ms_globals.tree;
function Re(n) {
  function t(o) {
    const l = E(), r = new Ce({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? O;
          return i.nodes = [...i.nodes, s], W({
            createPortal: k,
            node: O
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((a) => a.svelteInstance !== l), W({
              createPortal: k,
              node: O
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
function Oe(n) {
  const [t, o] = U(() => w(n));
  return H(() => {
    let l = !0;
    return n.subscribe((e) => {
      l && (l = !1, e === t) || o(e);
    });
  }, [n]), t;
}
function Pe(n) {
  const t = z(() => ee(n, (o) => o), [n]);
  return Oe(t);
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !ke.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function j(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(k(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = j(r.props.el);
          return h.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...h.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: s,
      type: i,
      useCapture: a
    }) => {
      o.addEventListener(i, s, a);
    });
  });
  const l = Array.from(n.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = j(e);
      t.push(...i), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function je(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const P = X(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = Z(), [s, i] = U([]);
  return H(() => {
    var p;
    if (!e.current || !n)
      return;
    let a = n;
    function f() {
      let d = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (d = a.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), je(r, d), o && d.classList.add(...o.split(" ")), l) {
        const _ = Ae(l);
        Object.keys(_).forEach((m) => {
          d.style[m] = _[m];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var x, b, y;
        (x = e.current) != null && x.contains(a) && ((b = e.current) == null || b.removeChild(a));
        const {
          portals: m,
          clonedElement: R
        } = j(n);
        return a = R, i(m), a.style.display = "contents", f(), (y = e.current) == null || y.appendChild(a), m.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      a.style.display = "contents", f(), (p = e.current) == null || p.appendChild(a);
    return () => {
      var d, _;
      a.style.display = "", (d = e.current) != null && d.contains(a) && ((_ = e.current) == null || _.removeChild(a)), u == null || u.disconnect();
    };
  }, [n, t, o, l, r]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le(n, t) {
  const o = z(() => h.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const i = w(e.props.node.slotIndex) || 0, a = w(s.props.node.slotIndex) || 0;
      return i - a === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (w(e.props.node.subSlotIndex) || 0) - (w(s.props.node.subSlotIndex) || 0) : i - a;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Pe(o);
}
const Ne = Re(({
  slots: n,
  children: t,
  ...o
}) => {
  var r, e, s, i, a, f;
  const l = Le(t);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ g.jsx(te.Group, {
      ...o,
      max: {
        ...o.max,
        popover: n["max.popover.title"] || n["max.popover.content"] ? {
          ...((e = o.max) == null ? void 0 : e.popover) || {},
          title: n["max.popover.title"] ? /* @__PURE__ */ g.jsx(P, {
            slot: n["max.popover.title"]
          }) : (i = (s = o.max) == null ? void 0 : s.popover) == null ? void 0 : i.title,
          content: n["max.popover.content"] ? /* @__PURE__ */ g.jsx(P, {
            slot: n["max.popover.content"]
          }) : (f = (a = o.max) == null ? void 0 : a.popover) == null ? void 0 : f.content
        } : (r = o.max) == null ? void 0 : r.popover
      },
      children: l.map((u, p) => /* @__PURE__ */ g.jsx(P, {
        slot: u
      }, p))
    })]
  });
});
export {
  Ne as AvatarGroup,
  Ne as default
};
