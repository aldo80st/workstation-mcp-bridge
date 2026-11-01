FROM node:22-bookworm-slim
ARG DC_VERSION=0.3.1
ARG SG_VERSION=4.2.1
RUN npm install --global --ignore-scripts "@wonderwhy-er/desktop-commander@${DC_VERSION}" "supergateway@${SG_VERSION}" \
  && npm cache clean --force \
  && mkdir -p /workspace /home/node/.config \
  && chown -R node:node /workspace /home/node
COPY --chmod=0755 images/workstation-mcp/entrypoint.sh /usr/local/bin/wmb-entrypoint
USER node
WORKDIR /workspace
EXPOSE 8765
ENTRYPOINT ["/usr/local/bin/wmb-entrypoint"]
