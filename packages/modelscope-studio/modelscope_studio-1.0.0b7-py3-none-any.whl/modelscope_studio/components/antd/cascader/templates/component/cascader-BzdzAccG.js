import { b as fe, g as _e, w as S } from "./Index-2ek-fwQI.js";
const R = window.ms_globals.React, de = window.ms_globals.React.forwardRef, T = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, L = window.ms_globals.React.useEffect, Y = window.ms_globals.React.useMemo, N = window.ms_globals.ReactDOM.createPortal, he = window.ms_globals.antd.Cascader;
function pe(e, t) {
  return fe(e, t);
}
var K = {
  exports: {}
}, F = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var me = R, ge = Symbol.for("react.element"), we = Symbol.for("react.fragment"), be = Object.prototype.hasOwnProperty, ye = me.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Q(e, t, r) {
  var o, l = {}, n = null, s = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) be.call(t, o) && !Ee.hasOwnProperty(o) && (l[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: ge,
    type: e,
    key: n,
    ref: s,
    props: l,
    _owner: ye.current
  };
}
F.Fragment = we;
F.jsx = Q;
F.jsxs = Q;
K.exports = F;
var g = K.exports;
const {
  SvelteComponent: Re,
  assign: W,
  binding_callbacks: M,
  check_outros: xe,
  children: X,
  claim_element: Z,
  claim_space: Ce,
  component_subscribe: q,
  compute_slots: ve,
  create_slot: Ie,
  detach: v,
  element: $,
  empty: z,
  exclude_internal_props: G,
  get_all_dirty_from_scope: Se,
  get_slot_changes: ke,
  group_outros: je,
  init: Fe,
  insert_hydration: k,
  safe_not_equal: Oe,
  set_custom_element_data: ee,
  space: Pe,
  transition_in: j,
  transition_out: A,
  update_slot_base: Te
} = window.__gradio__svelte__internal, {
  beforeUpdate: Le,
  getContext: Ne,
  onDestroy: Ae,
  setContext: De
} = window.__gradio__svelte__internal;
function U(e) {
  let t, r;
  const o = (
    /*#slots*/
    e[7].default
  ), l = Ie(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = $("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      t = Z(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = X(t);
      l && l.l(s), s.forEach(v), this.h();
    },
    h() {
      ee(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      k(n, t, s), l && l.m(t, null), e[9](t), r = !0;
    },
    p(n, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && Te(
        l,
        o,
        n,
        /*$$scope*/
        n[6],
        r ? ke(
          o,
          /*$$scope*/
          n[6],
          s,
          null
        ) : Se(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (j(l, n), r = !0);
    },
    o(n) {
      A(l, n), r = !1;
    },
    d(n) {
      n && v(t), l && l.d(n), e[9](null);
    }
  };
}
function Ve(e) {
  let t, r, o, l, n = (
    /*$$slots*/
    e[4].default && U(e)
  );
  return {
    c() {
      t = $("react-portal-target"), r = Pe(), n && n.c(), o = z(), this.h();
    },
    l(s) {
      t = Z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), X(t).forEach(v), r = Ce(s), n && n.l(s), o = z(), this.h();
    },
    h() {
      ee(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      k(s, t, a), e[8](t), k(s, r, a), n && n.m(s, a), k(s, o, a), l = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, a), a & /*$$slots*/
      16 && j(n, 1)) : (n = U(s), n.c(), j(n, 1), n.m(o.parentNode, o)) : n && (je(), A(n, 1, 1, () => {
        n = null;
      }), xe());
    },
    i(s) {
      l || (j(n), l = !0);
    },
    o(s) {
      A(n), l = !1;
    },
    d(s) {
      s && (v(t), v(r), v(o)), e[8](null), n && n.d(s);
    }
  };
}
function H(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function We(e, t, r) {
  let o, l, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const a = ve(n);
  let {
    svelteInit: c
  } = t;
  const m = S(H(t)), u = S();
  q(e, u, (d) => r(0, o = d));
  const _ = S();
  q(e, _, (d) => r(1, l = d));
  const i = [], h = Ne("$$ms-gr-react-wrapper"), {
    slotKey: f,
    slotIndex: w,
    subSlotIndex: p
  } = _e() || {}, x = c({
    parent: h,
    props: m,
    target: u,
    slot: _,
    slotKey: f,
    slotIndex: w,
    subSlotIndex: p,
    onDestroy(d) {
      i.push(d);
    }
  });
  De("$$ms-gr-react-wrapper", x), Le(() => {
    m.set(H(t));
  }), Ae(() => {
    i.forEach((d) => d());
  });
  function C(d) {
    M[d ? "unshift" : "push"](() => {
      o = d, u.set(o);
    });
  }
  function O(d) {
    M[d ? "unshift" : "push"](() => {
      l = d, _.set(l);
    });
  }
  return e.$$set = (d) => {
    r(17, t = W(W({}, t), G(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, t = G(t), [o, l, u, _, a, c, s, n, C, O];
}
class Me extends Re {
  constructor(t) {
    super(), Fe(this, t, We, Ve, Oe, {
      svelteInit: 5
    });
  }
}
const B = window.ms_globals.rerender, P = window.ms_globals.tree;
function qe(e) {
  function t(r) {
    const o = S(), l = new Me({
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
          }, a = n.parent ?? P;
          return a.nodes = [...a.nodes, s], B({
            createPortal: N,
            node: P
          }), n.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== o), B({
              createPortal: N,
              node: P
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
const ze = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ge(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const o = e[r];
    return typeof o == "number" && !ze.includes(r) ? t[r] = o + "px" : t[r] = o, t;
  }, {}) : {};
}
function D(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(N(R.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: R.Children.toArray(e._reactElement.props.children).map((l) => {
        if (R.isValidElement(l) && l.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = D(l.props.el);
          return R.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...R.Children.toArray(l.props.children), ...n]
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
      type: a,
      useCapture: c
    }) => {
      r.addEventListener(a, s, c);
    });
  });
  const o = Array.from(e.childNodes);
  for (let l = 0; l < o.length; l++) {
    const n = o[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = D(n);
      t.push(...a), r.appendChild(s);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Ue(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const y = de(({
  slot: e,
  clone: t,
  className: r,
  style: o
}, l) => {
  const n = T(), [s, a] = J([]);
  return L(() => {
    var _;
    if (!n.current || !e)
      return;
    let c = e;
    function m() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Ue(l, i), r && i.classList.add(...r.split(" ")), o) {
        const h = Ge(o);
        Object.keys(h).forEach((f) => {
          i.style[f] = h[f];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var p, x, C;
        (p = n.current) != null && p.contains(c) && ((x = n.current) == null || x.removeChild(c));
        const {
          portals: f,
          clonedElement: w
        } = D(e);
        return c = w, a(f), c.style.display = "contents", m(), (C = n.current) == null || C.appendChild(c), f.length > 0;
      };
      i() || (u = new window.MutationObserver(() => {
        i() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", m(), (_ = n.current) == null || _.appendChild(c);
    return () => {
      var i, h;
      c.style.display = "", (i = n.current) != null && i.contains(c) && ((h = n.current) == null || h.removeChild(c)), u == null || u.disconnect();
    };
  }, [e, t, r, o, l]), R.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function He(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Be(e, t = !1) {
  try {
    if (t && !He(e))
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
function b(e, t) {
  return Y(() => Be(e, t), [e, t]);
}
function Je({
  value: e,
  onValueChange: t
}) {
  const [r, o] = J(e), l = T(t);
  l.current = t;
  const n = T(r);
  return n.current = r, L(() => {
    l.current(r);
  }, [r]), L(() => {
    pe(e, n.current) || o(e);
  }, [e]), [r, o];
}
function te(e, t, r) {
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
      const u = m.split(".");
      u.forEach((w, p) => {
        s[w] || (s[w] = {}), p !== u.length - 1 && (s = n[w]);
      });
      const _ = o.slots[m];
      let i, h, f = (t == null ? void 0 : t.clone) ?? !1;
      _ instanceof Element ? i = _ : (i = _.el, h = _.callback, f = _.clone ?? !1), s[u[u.length - 1]] = i ? h ? (...w) => (h(u[u.length - 1], w), /* @__PURE__ */ g.jsx(y, {
        slot: i,
        clone: f
      })) : /* @__PURE__ */ g.jsx(y, {
        slot: i,
        clone: f
      }) : s[u[u.length - 1]], s = n;
    });
    const a = (t == null ? void 0 : t.children) || "children";
    return o[a] && (n[a] = te(o[a], t, `${l}`)), n;
  });
}
function Ye(e, t) {
  return e ? /* @__PURE__ */ g.jsx(y, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function I({
  key: e,
  setSlotParams: t,
  slots: r
}, o) {
  return r[e] ? (...l) => (t(e, l), Ye(r[e], {
    clone: !0,
    ...o
  })) : void 0;
}
function Ke(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Xe = qe(({
  slots: e,
  children: t,
  onValueChange: r,
  onChange: o,
  displayRender: l,
  elRef: n,
  getPopupContainer: s,
  tagRender: a,
  maxTagPlaceholder: c,
  dropdownRender: m,
  optionRender: u,
  showSearch: _,
  optionItems: i,
  options: h,
  setSlotParams: f,
  onLoadData: w,
  ...p
}) => {
  const x = b(s), C = b(l), O = b(a), d = b(u), ne = b(m), re = b(c), oe = typeof _ == "object" || e["showSearch.render"], E = Ke(_), le = b(E.filter), se = b(E.render), ce = b(E.sort), [ae, ie] = Je({
    onValueChange: r,
    value: p.value
  });
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ g.jsx(he, {
      ...p,
      ref: n,
      value: ae,
      options: Y(() => h || te(i, {
        clone: !0
      }), [h, i]),
      showSearch: oe ? {
        ...E,
        filter: le || E.filter,
        render: e["showSearch.render"] ? I({
          slots: e,
          setSlotParams: f,
          key: "showSearch.render"
        }) : se || E.render,
        sort: ce || E.sort
      } : _,
      loadData: w,
      optionRender: d,
      getPopupContainer: x,
      dropdownRender: e.dropdownRender ? I({
        slots: e,
        setSlotParams: f,
        key: "dropdownRender"
      }) : ne,
      displayRender: e.displayRender ? I({
        slots: e,
        setSlotParams: f,
        key: "displayRender"
      }) : C,
      tagRender: e.tagRender ? I({
        slots: e,
        setSlotParams: f,
        key: "tagRender"
      }) : O,
      onChange: (V, ...ue) => {
        o == null || o(V, ...ue), ie(V);
      },
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ g.jsx(y, {
        slot: e.suffixIcon
      }) : p.suffixIcon,
      expandIcon: e.expandIcon ? /* @__PURE__ */ g.jsx(y, {
        slot: e.expandIcon
      }) : p.expandIcon,
      removeIcon: e.removeIcon ? /* @__PURE__ */ g.jsx(y, {
        slot: e.removeIcon
      }) : p.removeIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ g.jsx(y, {
        slot: e.notFoundContent
      }) : p.notFoundContent,
      maxTagPlaceholder: e.maxTagPlaceholder ? I({
        slots: e,
        setSlotParams: f,
        key: "maxTagPlaceholder"
      }) : re || c,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ g.jsx(y, {
          slot: e["allowClear.clearIcon"]
        })
      } : p.allowClear
    })]
  });
});
export {
  Xe as Cascader,
  Xe as default
};
