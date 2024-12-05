import { b as $, g as ee, w as v } from "./Index-Zabc1nMz.js";
const b = window.ms_globals.React, X = window.ms_globals.React.forwardRef, O = window.ms_globals.React.useRef, z = window.ms_globals.React.useState, P = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, j = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Cascader;
function ne(n, t) {
  return $(n, t);
}
var G = {
  exports: {}
}, k = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var re = b, le = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, ce = re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, t, o) {
  var r, l = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (r in t) se.call(t, r) && !ae.hasOwnProperty(r) && (l[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) l[r] === void 0 && (l[r] = t[r]);
  return {
    $$typeof: le,
    type: n,
    key: e,
    ref: s,
    props: l,
    _owner: ce.current
  };
}
k.Fragment = oe;
k.jsx = U;
k.jsxs = U;
G.exports = k;
var g = G.exports;
const {
  SvelteComponent: ie,
  assign: N,
  binding_callbacks: A,
  check_outros: ue,
  children: H,
  claim_element: B,
  claim_space: de,
  component_subscribe: F,
  compute_slots: fe,
  create_slot: _e,
  detach: E,
  element: J,
  empty: D,
  exclude_internal_props: V,
  get_all_dirty_from_scope: pe,
  get_slot_changes: he,
  group_outros: me,
  init: ge,
  insert_hydration: x,
  safe_not_equal: be,
  set_custom_element_data: Y,
  space: we,
  transition_in: I,
  transition_out: L,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: Ce,
  onDestroy: ve,
  setContext: xe
} = window.__gradio__svelte__internal;
function M(n) {
  let t, o;
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
      t = J("svelte-slot"), l && l.c(), this.h();
    },
    l(e) {
      t = B(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = H(t);
      l && l.l(s), s.forEach(E), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      x(e, t, s), l && l.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      l && l.p && (!o || s & /*$$scope*/
      64) && Ee(
        l,
        r,
        e,
        /*$$scope*/
        e[6],
        o ? he(
          r,
          /*$$scope*/
          e[6],
          s,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (I(l, e), o = !0);
    },
    o(e) {
      L(l, e), o = !1;
    },
    d(e) {
      e && E(t), l && l.d(e), n[9](null);
    }
  };
}
function Ie(n) {
  let t, o, r, l, e = (
    /*$$slots*/
    n[4].default && M(n)
  );
  return {
    c() {
      t = J("react-portal-target"), o = we(), e && e.c(), r = D(), this.h();
    },
    l(s) {
      t = B(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(E), o = de(s), e && e.l(s), r = D(), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      x(s, t, c), n[8](t), x(s, o, c), e && e.m(s, c), x(s, r, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && I(e, 1)) : (e = M(s), e.c(), I(e, 1), e.m(r.parentNode, r)) : e && (me(), L(e, 1, 1, () => {
        e = null;
      }), ue());
    },
    i(s) {
      l || (I(e), l = !0);
    },
    o(s) {
      L(e), l = !1;
    },
    d(s) {
      s && (E(t), E(o), E(r)), n[8](null), e && e.d(s);
    }
  };
}
function W(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Re(n, t, o) {
  let r, l, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = fe(e);
  let {
    svelteInit: a
  } = t;
  const _ = v(W(t)), i = v();
  F(n, i, (d) => o(0, r = d));
  const f = v();
  F(n, f, (d) => o(1, l = d));
  const u = [], p = Ce("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: m,
    subSlotIndex: w
  } = ee() || {}, y = a({
    parent: p,
    props: _,
    target: i,
    slot: f,
    slotKey: h,
    slotIndex: m,
    subSlotIndex: w,
    onDestroy(d) {
      u.push(d);
    }
  });
  xe("$$ms-gr-react-wrapper", y), ye(() => {
    _.set(W(t));
  }), ve(() => {
    u.forEach((d) => d());
  });
  function C(d) {
    A[d ? "unshift" : "push"](() => {
      r = d, i.set(r);
    });
  }
  function Q(d) {
    A[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  return n.$$set = (d) => {
    o(17, t = N(N({}, t), V(d))), "svelteInit" in d && o(5, a = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, t = V(t), [r, l, i, f, c, a, s, e, C, Q];
}
class ke extends ie {
  constructor(t) {
    super(), ge(this, t, Re, Ie, be, {
      svelteInit: 5
    });
  }
}
const q = window.ms_globals.rerender, S = window.ms_globals.tree;
function Se(n) {
  function t(o) {
    const r = v(), l = new ke({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? S;
          return c.nodes = [...c.nodes, s], q({
            createPortal: j,
            node: S
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((a) => a.svelteInstance !== r), q({
              createPortal: j,
              node: S
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
      o(t);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const r = n[o];
    return typeof r == "number" && !Oe.includes(o) ? t[o] = r + "px" : t[o] = r, t;
  }, {}) : {};
}
function T(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(j(b.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: b.Children.toArray(n._reactElement.props.children).map((l) => {
        if (b.isValidElement(l) && l.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = T(l.props.el);
          return b.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...b.Children.toArray(l.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((l) => {
    n.getEventListeners(l).forEach(({
      listener: s,
      type: c,
      useCapture: a
    }) => {
      o.addEventListener(c, s, a);
    });
  });
  const r = Array.from(n.childNodes);
  for (let l = 0; l < r.length; l++) {
    const e = r[l];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = T(e);
      t.push(...c), o.appendChild(s);
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
const R = X(({
  slot: n,
  clone: t,
  className: o,
  style: r
}, l) => {
  const e = O(), [s, c] = z([]);
  return P(() => {
    var f;
    if (!e.current || !n)
      return;
    let a = n;
    function _() {
      let u = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (u = a.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), je(l, u), o && u.classList.add(...o.split(" ")), r) {
        const p = Pe(r);
        Object.keys(p).forEach((h) => {
          u.style[h] = p[h];
        });
      }
    }
    let i = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var w, y, C;
        (w = e.current) != null && w.contains(a) && ((y = e.current) == null || y.removeChild(a));
        const {
          portals: h,
          clonedElement: m
        } = T(n);
        return a = m, c(h), a.style.display = "contents", _(), (C = e.current) == null || C.appendChild(a), h.length > 0;
      };
      u() || (i = new window.MutationObserver(() => {
        u() && (i == null || i.disconnect());
      }), i.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      a.style.display = "contents", _(), (f = e.current) == null || f.appendChild(a);
    return () => {
      var u, p;
      a.style.display = "", (u = e.current) != null && u.contains(a) && ((p = e.current) == null || p.removeChild(a)), i == null || i.disconnect();
    };
  }, [n, t, o, r, l]), b.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le({
  value: n,
  onValueChange: t
}) {
  const [o, r] = z(n), l = O(t);
  l.current = t;
  const e = O(o);
  return e.current = o, P(() => {
    l.current(o);
  }, [o]), P(() => {
    ne(n, e.current) || r(n);
  }, [n]), [o, r];
}
function K(n, t, o) {
  return n.filter(Boolean).map((r, l) => {
    var a;
    if (typeof r != "object")
      return t != null && t.fallback ? t.fallback(r) : r;
    const e = {
      ...r.props,
      key: ((a = r.props) == null ? void 0 : a.key) ?? (o ? `${o}-${l}` : `${l}`)
    };
    let s = e;
    Object.keys(r.slots).forEach((_) => {
      if (!r.slots[_] || !(r.slots[_] instanceof Element) && !r.slots[_].el)
        return;
      const i = _.split(".");
      i.forEach((m, w) => {
        s[m] || (s[m] = {}), w !== i.length - 1 && (s = e[m]);
      });
      const f = r.slots[_];
      let u, p, h = (t == null ? void 0 : t.clone) ?? !1;
      f instanceof Element ? u = f : (u = f.el, p = f.callback, h = f.clone ?? !1), s[i[i.length - 1]] = u ? p ? (...m) => (p(i[i.length - 1], m), /* @__PURE__ */ g.jsx(R, {
        slot: u,
        clone: h
      })) : /* @__PURE__ */ g.jsx(R, {
        slot: u,
        clone: h
      }) : s[i[i.length - 1]], s = e;
    });
    const c = (t == null ? void 0 : t.children) || "children";
    return r[c] && (e[c] = K(r[c], t, `${l}`)), e;
  });
}
const Ne = Se(({
  slots: n,
  children: t,
  onValueChange: o,
  onChange: r,
  onLoadData: l,
  optionItems: e,
  options: s,
  ...c
}) => {
  const [a, _] = Le({
    onValueChange: o,
    value: c.value
  });
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ g.jsx(te.Panel, {
      ...c,
      value: a,
      options: Z(() => s || K(e, {
        clone: !0
      }), [s, e]),
      loadData: l,
      onChange: (i, ...f) => {
        r == null || r(i, ...f), _(i);
      },
      expandIcon: n.expandIcon ? /* @__PURE__ */ g.jsx(R, {
        slot: n.expandIcon
      }) : c.expandIcon,
      notFoundContent: n.notFoundContent ? /* @__PURE__ */ g.jsx(R, {
        slot: n.notFoundContent
      }) : c.notFoundContent
    })]
  });
});
export {
  Ne as CascaderPanel,
  Ne as default
};
