const {
  McpServer
} = require("@modelcontextprotocol/sdk/server/mcp.js");

const {
  StdioServerTransport
} = require("@modelcontextprotocol/sdk/server/stdio.js");

const {
  z
} = require("zod");

const fs = require("fs");
const path = require("path");
const { exec } = require("child_process");

const server = new McpServer({
  name: "software-dev-agent",
  version: "1.0.0"
});

const ROOT = path.resolve(__dirname, "..");

server.tool(
  "get_project_info",
  "Get basic information about the software project",
  {},
  async () => {
    return {
      content: [
        {
          type: "text",
          text: `
Software Development Agent

Language: Python
Framework: Flask
Testing: pytest

Workflow:
Issue → Code → Test → Pull Request → CI → Deploy
`
        }
      ]
    };
  }
);

server.tool(
  "read_file",
  "Read a file from the project",
  {
    filename: z.string()
  },
  async ({ filename }) => {

    const filePath = path.join(ROOT, filename);

    if (!fs.existsSync(filePath)) {
      return {
        content: [
          {
            type: "text",
            text: `File not found: ${filename}`
          }
        ]
      };
    }

    const content = fs.readFileSync(filePath, "utf8");

    return {
      content: [
        {
          type: "text",
          text: content
        }
      ]
    };
  }
);

server.tool(
  "run_tests",
  "Run the project's pytest tests",
  {},
  async () => {

    return new Promise((resolve) => {

      exec(
        "python -m pytest -v",
        { cwd: ROOT },
        (error, stdout, stderr) => {

          resolve({
            content: [
              {
                type: "text",
                text: stdout + stderr
              }
            ]
          });

        }
      );

    });
  }
);

async function main() {

  const transport = new StdioServerTransport();

  await server.connect(transport);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
