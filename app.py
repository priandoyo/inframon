import random
from datetime import datetime
import streamlit as st
import psutil

st.set_page_config(
    page_title="InfraMon",
    page_icon="🖥️",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.stApp {background:#0b1220;color:#e5edf8}
[data-testid="stHeader"] {background:transparent}
.block-container {padding-top:2rem;max-width:1200px}
h1,h2,h3 {color:#f4f7fb!important}
p,label,span {color:#c5d1e0}
[data-testid="stMetric"] {
 background:linear-gradient(145deg,#17243a,#111c2e);
 border:1px solid #263852;
 padding:16px;border-radius:12px;
}
div.stButton>button {
 border-radius:8px;border:1px solid #345477;
 background:#193454;color:white;font-weight:600;
}
div.stButton>button:hover {
 border-color:#58a6ff;color:white;
}
div[data-testid="stForm"] {
 background:#111c2e;border:1px solid #263852;
 padding:16px;border-radius:12px;
}
.panel {
 background:#111c2e;border:1px solid #263852;
 border-radius:12px;padding:16px;margin-bottom:10px;
}
.muted {color:#91a4bb;font-size:.85rem}
</style>
""", unsafe_allow_html=True)

# ---------- INITIAL DATA ----------
if "vms" not in st.session_state:
    st.session_state.vms = [
        {"name":"ojk-demo-vm01","cpu":2,"ram":4,"status":"Running"},
        {"name":"ojk-demo-vm02","cpu":4,"ram":8,"status":"Stopped"}
    ]

if "containers" not in st.session_state:
    st.session_state.containers = [
        {"name":"web-server","image":"nginx:latest","status":"Running"},
        {"name":"api-service","image":"python:3.12","status":"Stopped"}
    ]

if "deployments" not in st.session_state:
    st.session_state.deployments = [
        {"name":"hello-web","image":"nginx:latest",
         "replicas":3,"status":"Running"},
        {"name":"hello-api","image":"python:3.12",
         "replicas":2,"status":"Running"}
    ]

# ---------- FUNCTIONS ----------
def toggle(items, index):
    items[index]["status"] = (
        "Stopped" if items[index]["status"] == "Running"
        else "Running"
    )

def header(title, subtitle):
    st.title(title)
    st.caption(subtitle)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("# 🖥️ InfraMon")
    st.caption("Infrastructure Monitoring Lab")
    st.divider()

    page = st.radio(
        "WORKSPACE",
        ["Overview", "Virtual Machines",
         "Docker Containers", "Kubernetes"]
    )

    st.divider()
    st.markdown("**OJK Workshop · Basic Infrastructure**")
    st.caption("Demo mode · Resources are simulated")
    st.caption("Host metrics are real.")
    st.divider()
    st.caption(datetime.now().strftime("%H:%M:%S"))

# ---------- REAL HOST METRICS ----------
cpu = psutil.cpu_percent(interval=0.2)
memory = psutil.virtual_memory()
disk = psutil.disk_usage("/")

# ==================================================
# OVERVIEW
# ==================================================
if page == "Overview":

    header(
        "Infrastructure Overview",
        "A control panel for virtual machines, containers and Kubernetes workloads."
    )

    st.info(
        "DEMO ENVIRONMENT · Infrastructure resources are simulated. "
        "Host CPU, memory and disk metrics are real."
    )

    running = sum(
        x["status"] == "Running"
        for x in (
            st.session_state.vms
            + st.session_state.containers
            + st.session_state.deployments
        )
    )

    a,b,c,d = st.columns(4)

    a.metric("Virtual Machines", len(st.session_state.vms))
    b.metric("Containers", len(st.session_state.containers))
    c.metric("Deployments", len(st.session_state.deployments))
    d.metric("Running Resources", running)

    st.subheader("Host Machine Monitoring")

    x,y,z = st.columns(3)

    x.metric("CPU Usage", f"{cpu:.1f}%")
    y.metric("Memory Usage", f"{memory.percent:.1f}%")
    z.metric("Disk Usage", f"{disk.percent:.1f}%")

    x.progress(int(cpu))
    y.progress(int(memory.percent))
    z.progress(int(disk.percent))

    st.subheader("Infrastructure Layers")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="panel">
        <h3>🖥️ Virtual Machines</h3>
        <p class="muted">Compute layer</p>
        <b>Provision and manage virtual servers</b>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="panel">
        <h3>📦 Docker</h3>
        <p class="muted">Container layer</p>
        <b>Package and run applications</b>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="panel">
        <h3>☸️ Kubernetes</h3>
        <p class="muted">Orchestration layer</p>
        <b>Deploy and scale workloads</b>
        </div>
        """, unsafe_allow_html=True)

    st.caption(
        "A VM provides a machine, Docker packages an application, "
        "and Kubernetes manages container workloads."
    )

# ==================================================
# VIRTUAL MACHINES
# ==================================================
elif page == "Virtual Machines":

    header(
        "Virtual Machines",
        "Create and manage virtual servers."
    )

    with st.form("new_vm"):

        st.markdown("**Provision a virtual machine**")

        name = st.text_input(
            "VM name",
            placeholder="ojk-lab-vm03"
        )

        c1,c2 = st.columns(2)

        vcpu = c1.selectbox("vCPU", [1,2,4,8], index=1)
        ram = c2.selectbox("Memory (GB)", [1,2,4,8,16], index=2)

        submitted = st.form_submit_button("＋ Create VM")

        if submitted:
            if not name.strip():
                st.warning("Enter a VM name.")

            elif any(v["name"] == name.strip()
                     for v in st.session_state.vms):
                st.warning("VM already exists.")

            else:
                st.session_state.vms.append({
                    "name":name.strip(),
                    "cpu":vcpu,
                    "ram":ram,
                    "status":"Running"
                })
                st.success(f"{name} created.")
                st.rerun()

    st.subheader(
        f"VM Inventory · {len(st.session_state.vms)}"
    )

    if not st.session_state.vms:
        st.info("No virtual machines.")

    for i,vm in enumerate(st.session_state.vms):

        with st.container(border=True):

            left,mid,right = st.columns([3,2,2])

            left.markdown(f"**🖥️ {vm['name']}**")
            left.caption(
                f"{vm['cpu']} vCPU · {vm['ram']} GB RAM"
            )

            mid.markdown(f"**{vm['status']}**")

            if right.button(
                "Stop" if vm["status"] == "Running" else "Start",
                key=f"vm_toggle_{i}"
            ):
                toggle(st.session_state.vms,i)
                st.rerun()

            if right.button("Delete",key=f"vm_delete_{i}"):
                st.session_state.vms.pop(i)
                st.rerun()

    st.caption(
        "Simulation only: no real cloud VM is provisioned."
    )

# ==================================================
# DOCKER CONTAINERS
# ==================================================
elif page == "Docker Containers":

    header(
        "Docker Containers",
        "Explore container lifecycle and inventory."
    )

    with st.form("new_container"):

        st.markdown("**Create a container**")

        name = st.text_input(
            "Container name",
            placeholder="ojk-web"
        )

        image = st.selectbox(
            "Container image",
            ["nginx:latest","python:3.12",
             "redis:7","httpd:latest"]
        )

        submitted = st.form_submit_button("＋ Create Container")

        if submitted:
            if not name.strip():
                st.warning("Enter a container name.")

            elif any(c["name"] == name.strip()
                     for c in st.session_state.containers):
                st.warning("Container already exists.")

            else:
                st.session_state.containers.append({
                    "name":name.strip(),
                    "image":image,
                    "status":"Running"
                })
                st.success(f"Container {name} created.")
                st.rerun()

    st.subheader(
        f"Container Inventory · {len(st.session_state.containers)}"
    )

    if not st.session_state.containers:
        st.info("No containers.")

    for i,item in enumerate(st.session_state.containers):

        with st.container(border=True):

            left,mid,right = st.columns([3,2,2])

            left.markdown(f"**📦 {item['name']}**")
            left.caption(f"Image: {item['image']}")

            mid.markdown(f"**{item['status']}**")

            if right.button(
                "Stop" if item["status"] == "Running" else "Start",
                key=f"ct_toggle_{i}"
            ):
                toggle(st.session_state.containers,i)
                st.rerun()

            if right.button("Remove",key=f"ct_delete_{i}"):
                st.session_state.containers.pop(i)
                st.rerun()

    st.caption(
        "Simulation only: no Docker daemon is required."
    )

# ==================================================
# KUBERNETES
# ==================================================
elif page == "Kubernetes":

    header(
        "Kubernetes Workloads",
        "Deploy applications and scale replica counts."
    )

    with st.form("new_deployment"):

        st.markdown("**Deploy a workload**")

        name = st.text_input(
            "Deployment name",
            placeholder="ojk-frontend"
        )

        image = st.selectbox(
            "Container image",
            ["nginx:latest","python:3.12","redis:7"]
        )

        replicas = st.slider(
            "Initial replicas",1,5,2
        )

        submitted = st.form_submit_button("＋ Deploy")

        if submitted:
            if not name.strip():
                st.warning("Enter a deployment name.")

            elif any(d["name"] == name.strip()
                     for d in st.session_state.deployments):
                st.warning("Deployment already exists.")

            else:
                st.session_state.deployments.append({
                    "name":name.strip(),
                    "image":image,
                    "replicas":replicas,
                    "status":"Running"
                })
                st.success(
                    f"Deployment {name} created with {replicas} replicas."
                )
                st.rerun()

    st.subheader(
        f"Deployments · {len(st.session_state.deployments)}"
    )

    if not st.session_state.deployments:
        st.info("No deployments.")

    for i,dep in enumerate(st.session_state.deployments):

        with st.container(border=True):

            st.markdown(f"**☸️ {dep['name']}**")
            st.caption(
                f"Image: {dep['image']} · Status: {dep['status']}"
            )

            col1,col2,col3,col4 = st.columns([2,1,1,2])

            col1.metric("Desired pods",dep["replicas"])

            if col2.button(
                "−",
                key=f"k8s_minus_{i}",
                disabled=dep["replicas"] <= 1
            ):
                dep["replicas"] -= 1
                st.rerun()

            if col3.button(
                "＋",
                key=f"k8s_plus_{i}",
                disabled=dep["replicas"] >= 10
            ):
                dep["replicas"] += 1
                st.rerun()

            if col4.button(
                "Delete deployment",
                key=f"k8s_delete_{i}"
            ):
                st.session_state.deployments.pop(i)
                st.rerun()

            st.progress(100)
            st.caption(
                f"{dep['replicas']} / {dep['replicas']} "
                "simulated pods ready"
            )

    st.caption(
        "Simulation only: no Kubernetes API or cluster is contacted."
    )

# ---------- FOOTER ----------
st.divider()
st.caption(
    "InfraMon v1.0 · OJK Infrastructure Workshop · Educational demonstration"
)
