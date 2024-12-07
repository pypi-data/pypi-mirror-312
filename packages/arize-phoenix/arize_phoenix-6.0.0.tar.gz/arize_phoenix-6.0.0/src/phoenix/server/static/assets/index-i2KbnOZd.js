import{r as c,j as e,du as v,l as n,U as F,R as w,D as E,ba as R,dv as S,dw as L,dx as r,dy as z,dz as k,t as A,dA as $}from"./vendor-UNccFYqq.js";import{D as C,d as I,$ as _,G as j,t as T,a4 as D}from"./vendor-arizeai-gSIqhzZY.js";import{E as O,L as G,R as N,r as B,b as M,F as U,A as J,c as K,d as W,P as q,h as H,M as V,e as m,D as Y,f as Q,g as X,i as Z,j as ee,k as re,T as ae,p as te,l as g,n as oe,o as ne,q as u,s as se,t as h,v as x,w as le,x as ie,y as de,z as ce,B as pe,C as f,G as me,S as ge,H as ue,I as he,J as xe,K as fe,N as be}from"./pages-BfYVoiUE.js";import{c5 as ye,$ as Pe,R as ve,c6 as Fe,c7 as we}from"./components-Bo-xjXoV.js";import"./vendor-three-DwGkEfCM.js";import"./vendor-recharts-CVVyA2X0.js";import"./vendor-codemirror-fSYjW3f-.js";(function(){const s=document.createElement("link").relList;if(s&&s.supports&&s.supports("modulepreload"))return;for(const t of document.querySelectorAll('link[rel="modulepreload"]'))d(t);new MutationObserver(t=>{for(const o of t)if(o.type==="childList")for(const l of o.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&d(l)}).observe(document,{childList:!0,subtree:!0});function i(t){const o={};return t.integrity&&(o.integrity=t.integrity),t.referrerPolicy&&(o.referrerPolicy=t.referrerPolicy),t.crossOrigin==="use-credentials"?o.credentials="include":t.crossOrigin==="anonymous"?o.credentials="omit":o.credentials="same-origin",o}function d(t){if(t.ep)return;t.ep=!0;const o=i(t);fetch(t.href,o)}})();const b="arize-phoenix-feature-flags",p={__RESET__:!1};function Ee(){const a=localStorage.getItem(b);if(!a)return p;try{const s=JSON.parse(a);return Object.assign({},p,s)}catch{return p}}const y=c.createContext(null);function Re(){const a=w.useContext(y);if(a===null)throw new Error("useFeatureFlags must be used within a FeatureFlagsProvider");return a}function Se(a){const[s,i]=c.useState(Ee()),d=t=>{localStorage.setItem(b,JSON.stringify(t)),i(t)};return e(y.Provider,{value:{featureFlags:s,setFeatureFlags:d},children:e(Le,{children:a.children})})}function Le(a){const{children:s}=a,{featureFlags:i,setFeatureFlags:d}=Re(),[t,o]=c.useState(!1);return v("ctrl+shift+f",()=>o(!0)),n(F,{children:[s,e(j,{type:"modal",isDismissable:!0,onDismiss:()=>o(!1),children:t&&e(C,{title:"Feature Flags",children:e(I,{height:"size-1000",padding:"size-100",children:Object.keys(i).map(l=>e(_,{isSelected:i[l],onChange:P=>d({...i,[l]:P}),children:l},l))})})})]})}function ze(){return e(R,{styles:a=>E`
        body {
          background-color: var(--ac-global-color-grey-75);
          color: var(--ac-global-text-color-900);
          font-family: "Roboto";
          font-size: ${a.typography.sizes.medium.fontSize}px;
          margin: 0;
          overflow: hidden;
          #root,
          #root > div[data-overlay-container="true"],
          #root > div[data-overlay-container="true"] > .ac-theme {
            height: 100vh;
          }
        }

        /* Remove list styling */
        ul {
          display: block;
          list-style-type: none;
          margin-block-start: none;
          margin-block-end: 0;
          padding-inline-start: 0;
          margin-block-start: 0;
        }

        /* A reset style for buttons */
        .button--reset {
          background: none;
          border: none;
          padding: 0;
        }
        /* this css class is added to html via modernizr @see modernizr.js */
        .no-hiddenscroll {
          /* Works on Firefox */
          * {
            scrollbar-width: thin;
            scrollbar-color: var(--ac-global-color-grey-300)
              var(--ac-global-color-grey-400);
          }

          /* Works on Chrome, Edge, and Safari */
          *::-webkit-scrollbar {
            width: 14px;
          }

          *::-webkit-scrollbar-track {
            background: var(--ac-global-color-grey-100);
          }

          *::-webkit-scrollbar-thumb {
            background-color: var(--ac-global-color-grey-75);
            border-radius: 8px;
            border: 1px solid var(--ac-global-color-grey-300);
          }
        }

        :root {
          --px-blue-color: ${a.colors.arizeBlue};

          --px-flex-gap-sm: ${a.spacing.margin4}px;
          --px-flex-gap-sm: ${a.spacing.margin8}px;

          --px-section-background-color: ${a.colors.gray500};

          /* An item is a typically something in a list */
          --px-item-background-color: ${a.colors.gray800};
          --px-item-border-color: ${a.colors.gray600};

          --px-spacing-sm: ${a.spacing.padding4}px;
          --px-spacing-med: ${a.spacing.padding8}px;
          --px-spacing-lg: ${a.spacing.padding16}px;

          --px-border-radius-med: ${a.borderRadius.medium}px;

          --px-font-size-sm: ${a.typography.sizes.small.fontSize}px;
          --px-font-size-med: ${a.typography.sizes.medium.fontSize}px;
          --px-font-size-lg: ${a.typography.sizes.large.fontSize}px;

          --px-gradient-bar-height: 8px;

          --px-nav-collapsed-width: 45px;
          --px-nav-expanded-width: 200px;
        }

        .ac-theme--dark {
          --px-primary-color: #9efcfd;
          --px-primary-color--transparent: rgb(158, 252, 253, 0.2);
          --px-reference-color: #baa1f9;
          --px-reference-color--transparent: #baa1f982;
          --px-corpus-color: #92969c;
          --px-corpus-color--transparent: #92969c63;
        }
        .ac-theme--light {
          --px-primary-color: #00add0;
          --px-primary-color--transparent: rgba(0, 173, 208, 0.2);
          --px-reference-color: #4500d9;
          --px-reference-color--transparent: rgba(69, 0, 217, 0.2);
          --px-corpus-color: #92969c;
          --px-corpus-color--transparent: #92969c63;
        }
      `})}const ke=S(L(n(r,{path:"/",errorElement:e(O,{}),children:[e(r,{path:"/login",element:e(G,{})}),e(r,{path:"/reset-password",element:e(N,{}),loader:B}),e(r,{path:"/reset-password-with-token",element:e(M,{})}),e(r,{path:"/forgot-password",element:e(U,{})}),e(r,{element:e(J,{}),loader:K,children:n(r,{element:e(W,{}),children:[e(r,{path:"/profile",handle:{crumb:()=>"profile"},element:e(q,{})}),e(r,{index:!0,loader:H}),n(r,{path:"/model",handle:{crumb:()=>"model"},element:e(V,{}),children:[e(r,{index:!0,element:e(m,{})}),e(r,{element:e(m,{}),children:e(r,{path:"dimensions",children:e(r,{path:":dimensionId",element:e(Y,{}),loader:Q})})}),e(r,{path:"embeddings",children:e(r,{path:":embeddingDimensionId",element:e(X,{}),loader:Z,handle:{crumb:a=>a.embedding.name}})})]}),n(r,{path:"/projects",handle:{crumb:()=>"projects"},element:e(ee,{}),children:[e(r,{index:!0,element:e(re,{})}),n(r,{path:":projectId",element:e(ae,{}),loader:te,handle:{crumb:a=>a.project.name},children:[e(r,{index:!0,element:e(g,{})}),e(r,{element:e(g,{}),children:e(r,{path:"traces/:traceId",element:e(oe,{})})})]})]}),n(r,{path:"/datasets",handle:{crumb:()=>"datasets"},children:[e(r,{index:!0,element:e(ne,{})}),n(r,{path:":datasetId",loader:u,handle:{crumb:a=>a.dataset.name},children:[n(r,{element:e(se,{}),loader:u,children:[e(r,{index:!0,element:e(h,{}),loader:x}),e(r,{path:"experiments",element:e(h,{}),loader:x}),e(r,{path:"examples",element:e(le,{}),loader:ie,children:e(r,{path:":exampleId",element:e(de,{})})})]}),e(r,{path:"compare",handle:{crumb:()=>"compare"},loader:ce,element:e(pe,{})})]})]}),n(r,{path:"/playground",handle:{crumb:()=>"Playground"},children:[e(r,{index:!0,element:e(f,{})}),e(r,{path:"datasets/:datasetId",element:e(f,{}),children:e(r,{path:"examples/:exampleId",element:e(me,{})})}),e(r,{path:"spans/:spanId",element:e(ge,{}),loader:ue,handle:{crumb:a=>a.span.__typename==="Span"?`span ${a.span.context.spanId}`:"span unknown"}})]}),e(r,{path:"/apis",element:e(he,{}),handle:{crumb:()=>"APIs"}}),e(r,{path:"/settings",element:e(xe,{}),handle:{crumb:()=>"Settings"}})]})})]})),{basename:window.Config.basename});function Ae(){return e(z,{router:ke})}function $e(){return e(fe,{children:e(ye,{children:e(Ce,{})})})}function Ce(){const{theme:a}=Pe();return e(D,{theme:a,children:e(k,{theme:T,children:n(A.RelayEnvironmentProvider,{environment:ve,children:[e(ze,{}),e(Se,{children:e(Fe,{children:e(be,{children:e(c.Suspense,{children:e(we,{children:e(Ae,{})})})})})})]})})})}const Ie=document.getElementById("root"),_e=$.createRoot(Ie);_e.render(e($e,{}));
