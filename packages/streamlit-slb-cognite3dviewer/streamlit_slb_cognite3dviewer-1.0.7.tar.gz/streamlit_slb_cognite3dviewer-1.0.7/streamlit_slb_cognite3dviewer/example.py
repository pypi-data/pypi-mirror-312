import os
import base64
import streamlit as st
import gzip
import json
from typing import List

from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthInteractive, OAuthClientCredentials
from streamlit_slb_cognite3dviewer import streamlit_slb_cognite3dviewer

from models.viewer_data import ViewerData
from models.deck import Deck
from models.beacon import Beacon
from models.camera import Camera
from models.coordinate import Coordinate
from pandas import DataFrame
from helpers.cognite_helper import get_deck_list

def assign_auth(project_name):
        
    if project_name == "slb-test":        
        tenant_id = os.environ.get("CDF_SLBTEST_TENANT_ID") 
        client_id = os.environ.get("CDF_SLBTEST_CLIENT_ID") 
        client_secret = os.environ.get("CDF_SLBTEST_CLIENT_SECRET")
        cluster = os.environ.get("CDF_SLBTEST_CLUSTER")     
    elif project_name == "petronas-pma-dev" or project_name == "petronas-pma-playground":
        tenant_id = os.environ.get("CDF_PETRONASPMA_TENANT_ID") 
        cluster = os.environ.get("CDF_PETRONASPMA_CLUSTER") 
        client_id = os.environ.get("CDF_PETRONASPMA_CLIENT_ID") 
        client_secret = ""
    elif project_name == "hess-malaysia-dev":
        tenant_id = os.environ.get("CDF_HESSDEV_TENANT_ID") 
        client_id = os.environ.get("CDF_HESSDEV_CLIENT_ID") 
        client_secret = os.environ.get("CDF_HESSDEV_CLIENT_SECRET") 
        cluster = os.environ.get("CDF_HESSDEV_CLUSTER") 
    elif project_name == "hess-malaysia-prod":
        tenant_id = os.environ.get("CDF_HESSPROD_TENANT_ID") 
        client_id = os.environ.get("CDF_HESSPROD_CLIENT_ID") 
        client_secret = os.environ.get("CDF_HESSPROD_CLIENT_SECRET") 
        cluster = os.environ.get("CDF_HESSPROD_CLUSTER")     
    elif project_name == "mubadala-dev":
        tenant_id = os.environ.get("CDF_MUBADALADEV_TENANT_ID") 
        cluster = os.environ.get("CDF_MUBADALADEV_CLUSTER")
        client_id = os.environ.get("CDF_MUBADALADEV_CLIENT_ID") 
        client_secret = os.environ.get("CDF_MUBADALADEV_CLIENT_SECRET") 
           
    base_url = f"https://{cluster}.cognitedata.com"
    scopes = [f"{base_url}/.default"]
    
    return {
        "tenant_id": tenant_id, 
        "client_id": client_id, 
        "client_secret": client_secret, 
        "cluster": cluster,
        "base_url": base_url,
        "project_name": project_name,
        "scopes": scopes
    }

def interactive_client(project_name):
    
    auth_data: any = assign_auth(project_name)
    
    """Function to instantiate the CogniteClient, using the interactive auth flow"""
    return CogniteClient(
        ClientConfig(
            client_name=auth_data['project_name'],
            project=auth_data['project_name'],
            base_url=auth_data['base_url'],
            credentials=OAuthInteractive(
                authority_url=f"https://login.microsoftonline.com/{auth_data['tenant_id']}",
                client_id=auth_data['client_id'],
                scopes=auth_data['scopes'],
            ),
        )
    )

def client_credentials(project_name):
    
    auth_data = assign_auth(project_name)

    credentials = OAuthClientCredentials(
        token_url=f"https://login.microsoftonline.com/{auth_data['tenant_id']}/oauth2/v2.0/token", 
        client_id=auth_data['client_id'], 
        client_secret= auth_data['client_secret'],
        scopes=auth_data['scopes']
    )

    config = ClientConfig(
        client_name=auth_data['project_name'],
        project=auth_data['project_name'],
        base_url=auth_data['base_url'],
        credentials=credentials,
    )
    client = CogniteClient(config)

    return client

def connect(project_name):
    auth = assign_auth(project_name=project_name)  
    if auth["client_secret"] == "":
        return interactive_client(project_name)
    else:
        return client_credentials(project_name)

st.set_page_config(layout='wide')
st.subheader("Streamlit Slb ThreeDViewer Examples")

client: CogniteClient = connect("mubadala-dev")

selected_deck_external_id: int = None
selected_deck_image_id: int = None
imagelist_df: DataFrame = None
viewer_data: ViewerData = None
data_3d = None
       
def render_selectbox() -> int:
    deckData = get_deck_list(client=client)
    options = {item["name"]: item["externalId"] for item in deckData["listDeck"]["items"]}
    deck_name = st.selectbox(label="Select Deck", options=options.keys())
    selected_deck_external_id = options[deck_name]
    return selected_deck_external_id

def get_image_from_id(image_id) -> str:
    image_bytes = client.files.download_bytes(id=image_id)
    base64_str = base64.b64encode(image_bytes).decode("utf-8")
    return base64_str

def get_data() -> ViewerData:
    global viewer_data    
    
    viewer_data = ViewerData(name="3D Viewer", height=800)
    # deckinfo: Deck = get_deck_and_beacon_info(selected_deck_external_id)
    deckinfo: Deck = get_deck_and_camera_info(selected_deck_external_id)
    viewer_data.deck = deckinfo
   
    return viewer_data

def get_deck_and_beacon_info(deck_external_id: str) -> Deck:   
    
    global selected_deck_image_id
    
    deckInfo: Deck = None
    deckData = get_deck_info_by_external_id(deck_external_id=deck_external_id)
       
    if deckData:       
        deck_id = deckData["getDeckById"]["items"][0]["id"]
        deck_external_id = deckData["getDeckById"]["items"][0]["externalId"]
        deck_name = deckData["getDeckById"]["items"][0]["name"]
        deck_image_id = deckData["getDeckById"]["items"][0]["imageId"]
        selected_deck_image_id = int(deckData["getDeckById"]["items"][0]["imageIdStr"])
        deckInfo = Deck(id=deck_id, external_id=deck_external_id, name=deck_name, image_id=deck_image_id, beacons=[], cameras=[])    
        # beacons
        if deckData["getDeckById"]["items"][0]["beacons"]["items"] is not None and len(deckData["getDeckById"]["items"][0]["beacons"]["items"]) > 0:
            for beacon in deckData["getDeckById"]["items"][0]["beacons"]["items"]:
                beaconId = beacon["id"]
                beaconExternalId = beacon["externalId"]
                beaconName = beacon["name"]
                beaconMac = beacon["macAddress"]
                beaconZone = beacon["zone"]
                beaconRadius = beacon["radius"]
                beaconWidthSegment = beacon["widthSegment"]
                beacinHeightSegment = beacon["heightSegment"]
                beaconColor = beacon["color"]
                beaconSignalRadius = beacon["signalRadius"]
                beaconFadeSpeed = beacon["fadeSpeed"]
                beaconExpandSpeed = beacon["expandSpeed"]
                beaconMaxScale = beacon["maxScale"]
                beaconLocation=beacon["deviceLocation"]
                
                beaconInfo: Beacon = Beacon(
                    id=beaconId, 
                    external_id=beaconExternalId, 
                    name=beaconName, 
                    macAddress=beaconMac,
                    zone=beaconZone,
                    radius=beaconRadius,
                    widthSegment=beaconWidthSegment,
                    heightSegment=beacinHeightSegment,
                    color=beaconColor,
                    signalRadius=beaconSignalRadius,
                    fadeSpeed=beaconFadeSpeed,
                    expandSpeed=beaconExpandSpeed,
                    maxScale=beaconMaxScale,
                    deviceLocation=beaconLocation
                )
                deckInfo.beacons.append(beaconInfo)        
    else:
        print("No data found for " + deck_external_id)
    
    return deckInfo

def get_deck_and_camera_info(deck_external_id: str) -> Deck:   
    
    global selected_deck_image_id
    
    deckInfo: Deck = None
    deckData = get_deck_info_by_external_id(deck_external_id=deck_external_id)
        
    if deckData:       
        deck_id = deckData["getDeckById"]["items"][0]["id"]
        deck_external_id = deckData["getDeckById"]["items"][0]["externalId"]
        deck_name = deckData["getDeckById"]["items"][0]["name"]
        deck_image_id = deckData["getDeckById"]["items"][0]["imageId"]
        selected_deck_image_id = int(deckData["getDeckById"]["items"][0]["imageIdStr"])
        deckInfo = Deck(id=deck_id, external_id=deck_external_id, name=deck_name, image_id=deck_image_id, beacons=[], cameras=[])    
        # cameras
        if deckData["getDeckById"]["items"][0]["cameras"]["items"] is not None and len(deckData["getDeckById"]["items"][0]["cameras"]["items"]) > 0:
            for camera in deckData["getDeckById"]["items"][0]["cameras"]["items"]:
                cameraId = camera["id"]
                cameraExternalId = camera["externalId"]
                cameraName = camera["name"]
                cameraLocation = camera["deviceLocation"]
                
                cameraInfo: Camera = Camera(
                    id=cameraId,
                    external_id=cameraExternalId,
                    name=cameraName,
                    deviceLocation=cameraLocation
                )   
                deckInfo.cameras.append(cameraInfo) 
        
    else:
        print("No data found for " + deck_external_id)
    
    return deckInfo


def get_deck_info_by_external_id(deck_external_id: str) -> dict[str, any]:    
    query = """
        query GetDeckByExternalId {
            getDeckById(instance: {space: "threed_viewer", externalId: "%s"}) {
                items {
                    code
                    createdTime
                    externalId
                    id
                    imageId
                    imageIdStr
                    lastUpdatedTime
                    name
                    planeColor
                    planeHeight
                    planePosition {
                        items {
                            x
                            y
                            z
                        }
                    }
                    planeRotation
                    planeThickness
                    planeWidth
                    beacons {
                        items {
                            id
                            externalId
                            color
                            deviceLocation {
                                    items {
                                    x
                                    y
                                    z
                                }
                            }
                            expandSpeed
                            fadeSpeed
                            heightSegment
                            macAddress
                            maxScale
                            name
                            radius
                            signalRadius
                            widthSegment
                            zone
                        }
                    }
                    cameras {
                        items {
                            id
                            externalId
                            name
                            deviceLocation {
                                items {
                                    x
                                    y
                                    z
                                    externalId
                                }
                            }
                        }
                    }
                }
            }
        }
    """ % (deck_external_id)
    deck_info = client.data_modeling.graphql.query(
        id=("threed_viewer", "PlatformDeck", "12"),
        query=query
    )
    return deck_info

selected_deck_external_id = render_selectbox()
col1, col2 = st.columns(2)

with col1:
    threed_container = st.empty()
with col2:
    data_container = st.empty()

@st.fragment()
def render_viewer():      
    global viewer_data    
    global data_3d
    deck_image_str = get_image_from_id(selected_deck_image_id)
    floating_content = "<div style='font-weight:bold;color:red;margin: 10px;'>Testing</div>"
    model_path = "/models"
    with threed_container:
        # data_3d = streamlit_slb_cognite3dviewer(height=800, deck_image=deck_image_str, enable_animation=False, data=viewer_data.to_json())
        data_3d = streamlit_slb_cognite3dviewer(height=800, deck_image=deck_image_str, enable_animation=False, floating_content=floating_content, model_path=model_path, data=viewer_data.to_json())
    show_3d_data()

@st.fragment()
def show_3d_data():    
    data_container.empty()
    with data_container:
        if data_3d is not None:
            st.write(data_3d)

viewer_data = get_data()
render_viewer()



