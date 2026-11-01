FROM node:22-trixie-slim@sha256:2117f713a417f3aff682ac8f5bc2ebbdf1beed51f36e67ab1e0fd3866b6d2d8f AS dependencies
WORKDIR /opt/runtime
COPY images/workstation-mcp/package.json images/workstation-mcp/package-lock.json ./
RUN npm ci --omit=dev --ignore-scripts && npm cache clean --force

FROM node:22-trixie-slim@sha256:2117f713a417f3aff682ac8f5bc2ebbdf1beed51f36e67ab1e0fd3866b6d2d8f
COPY --from=dependencies /opt/runtime /opt/runtime
ENV PATH="/opt/runtime/node_modules/.bin:${PATH}"
RUN mkdir -p /workspace /home/node/.config \
  && chown -R node:node /workspace /home/node \
  && rm -rf /usr/local/lib/node_modules/npm /usr/local/bin/npm /usr/local/bin/npx
COPY images/workstation-mcp/configure.mjs /usr/local/lib/wmb/configure.mjs
COPY --chmod=0755 images/workstation-mcp/entrypoint.sh /usr/local/bin/wmb-entrypoint
USER node
WORKDIR /workspace
EXPOSE 8765
ENTRYPOINT ["/usr/local/bin/wmb-entrypoint"]
